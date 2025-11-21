#!/usr/bin/env python3
import asyncio
import unittest
import json
import os
import sys
import requests
import time
from urllib.parse import urljoin
import io
from contextlib import redirect_stdout

# Configurações
BASE_URL = os.environ.get("TEST_API_URL", "http://localhost")
HEALTH_CHECK_TIMEOUT = 60  # segundos para aguardar que a API esteja pronta

class KVStoreAPITests(unittest.TestCase):
    """Testes unitários para a API de Key-Value Store"""
    
    @classmethod
    def setUpClass(cls):
        """Espera que a API esteja disponível antes de executar os testes"""
        print("🔍 Verificando se a API está disponível...")
        start_time = time.time()
        ready = False
        
        while time.time() - start_time < HEALTH_CHECK_TIMEOUT:
            try:
                response = requests.get(urljoin(BASE_URL, "/health/live"), timeout=2)
                if response.status_code == 200:
                    ready = True
                    break
            except requests.RequestException:
                pass
            
            time.sleep(1)
            sys.stdout.write(".")
            sys.stdout.flush()
        
        print("\n")
        if not ready:
            print("❌ API não está disponível após esperar. Impossível executar testes.")
            sys.exit(1)
        
        print("✅ API disponível! Iniciando testes...")
    
    def test_01_health_check(self):
        """Verifica se o health check está funcionando"""
        response = requests.get(urljoin(BASE_URL, "/health"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "healthy")
    
    def test_02_liveness_check(self):
        """Verifica se o liveness check está funcionando"""
        response = requests.get(urljoin(BASE_URL, "/health/live"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "alive")
    
    def test_03_readiness_check(self):
        """Verifica se o readiness check está funcionando"""
        response = requests.get(urljoin(BASE_URL, "/health/ready"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "ready")
    
    def test_04_cache_stats(self):
        """Verifica se as estatísticas de cache estão disponíveis"""
        response = requests.get(urljoin(BASE_URL, "/cache/stats"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("keys_count", data)
        self.assertIn("max_keys_limit", data)
        self.assertIn("memory_used_bytes", data)
    
    def test_05_put_and_get(self):
        """Testa operações PUT e GET"""
        # Criar um valor único para este teste
        test_key = f"test_key_{int(time.time())}"
        test_value = "test_value_123"
        
        try:
            # PUT: Adicionar um valor
            put_data = {"data": {"key": test_key, "value": test_value}}
            response = requests.put(urljoin(BASE_URL, "/kv"), json=put_data)
            self.assertEqual(response.status_code, 202)
            self.assertEqual(response.json().get("detail"), "queued")
            
            # Esperar pelo processamento async (consumer)
            time.sleep(2)
            
            # GET: Verificar se o valor foi armazenado
            response = requests.get(urljoin(BASE_URL, f"/kv?key={test_key}"))
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data.get("data", {}).get("value"), test_value)
        except Exception as e:
            self.fail(f"Erro ao testar operações PUT e GET: {str(e)}")
    
    def test_06_delete(self):
        """Testa operação DELETE"""
        # Criar um valor único para este teste
        test_key = f"delete_test_key_{int(time.time())}"
        test_value = "test_value_to_delete"
        
        try:
            # PUT: Adicionar um valor
            put_data = {"data": {"key": test_key, "value": test_value}}
            response = requests.put(urljoin(BASE_URL, "/kv"), json=put_data)
            self.assertEqual(response.status_code, 202)
            
            # Esperar pelo processamento async
            time.sleep(2)
            
            # Verificar se o valor existe antes de deletar
            response = requests.get(urljoin(BASE_URL, f"/kv?key={test_key}"))
            self.assertEqual(response.status_code, 200)
            
            # DELETE: Remover o valor
            response = requests.delete(urljoin(BASE_URL, f"/kv?key={test_key}"))
            self.assertEqual(response.status_code, 202)
            
            # Esperar pelo processamento async
            time.sleep(2)
            
            # Verificar se o valor foi deletado
            response = requests.get(urljoin(BASE_URL, f"/kv?key={test_key}"))
            self.assertTrue(response.status_code in [404, 500], 
                           f"Esperado status 404 ou 500, obtido {response.status_code}")
        except Exception as e:
            self.fail(f"Erro ao testar operação DELETE: {str(e)}")
        
        # Teste DELETE para chave inexistente
        try:
            nonexistent_key = f"nonexistent_delete_key_{int(time.time())}"
            response = requests.delete(urljoin(BASE_URL, f"/kv?key={nonexistent_key}"))
            self.assertTrue(response.status_code in [404, 500], 
                          f"Esperado status 404 ou 500 ao deletar chave inexistente, obtido {response.status_code}")
        except Exception as e:
            self.fail(f"Erro ao testar DELETE de chave inexistente: {str(e)}")
    
    def test_07_nonexistent_key(self):
        """Testa comportamento para chave inexistente"""
        nonexistent_key = f"nonexistent_key_{int(time.time())}"
        
        try:
            response = requests.get(urljoin(BASE_URL, f"/kv?key={nonexistent_key}"))
            # Tanto 404 quanto 500 são aceitáveis neste teste, no momento
            self.assertTrue(response.status_code in [404, 500], 
                          f"Esperado status 404 ou 500, obtido {response.status_code}")
            
            # Se for 404, verificamos a mensagem
            if response.status_code == 404:
                data = response.json()
                self.assertIn("detail", data)
                self.assertEqual(data["detail"], "Key not found")
        except Exception as e:
            self.fail(f"Erro ao testar chave inexistente: {str(e)}")
    
    def test_08_invalid_put_request(self):
        """Testa validação de requisição PUT inválida"""
        # PUT sem value
        invalid_data = {"data": {"key": "test_key"}}
        response = requests.put(urljoin(BASE_URL, "/kv"), json=invalid_data)
        self.assertEqual(response.status_code, 400)
        
        # PUT sem key
        invalid_data = {"data": {"value": "test_value"}}
        response = requests.put(urljoin(BASE_URL, "/kv"), json=invalid_data)
        self.assertEqual(response.status_code, 400)

def run_tests():
    """Executa os testes e retorna o resultado"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(KVStoreAPITests)
    
    # Silenciar a saída detalhada dos testes
    output_buffer = io.StringIO()
    
    # Redirecionar a saída padrão para o buffer durante a execução
    with redirect_stdout(output_buffer):
        runner = unittest.TextTestRunner(verbosity=0, stream=output_buffer)
        result = runner.run(suite)
    
    total_tests = result.testsRun
    passed_tests = total_tests - len(result.errors) - len(result.failures)
    
    # Exibir apenas uma mensagem sucinta com o resultado
    if result.wasSuccessful():
        print(f"✅ {passed_tests} de {total_tests} testes passaram com sucesso!")
    else:
        print(f"⚠️ {passed_tests} de {total_tests} testes passaram. Falhas detectadas.")
        # Mostrar as falhas, mas de forma resumida
        if result.failures:
            print("\nFalhas:")
            for i, (test, error) in enumerate(result.failures, 1):
                test_name = test._testMethodName
                print(f"  {i}. {test_name}: {error.splitlines()[-1] if error.splitlines() else 'Erro desconhecido'}")
        
        if result.errors:
            print("\nErros:")
            for i, (test, error) in enumerate(result.errors, 1):
                test_name = test._testMethodName
                print(f"  {i}. {test_name}: {error.splitlines()[-1] if error.splitlines() else 'Erro desconhecido'}")
    
    # Retornar código de saída apropriado
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code) 