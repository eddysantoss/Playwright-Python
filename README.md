# Playwright Python Automation

Projeto de automação de testes usando Playwright com Python e pytest.

## Estrutura do projeto

- `tests/`: casos de teste pytest
- `pages/`: page objects para as páginas do sistema
- `conftest.py`: fixtures de teste, incluindo credenciais e carregamento de `.env`
- `pytest.ini`: configuração do pytest para `tests/` e `--headed`

## Como usar

1. Ative o ambiente virtual:
   ```powershell
   & "C:/Projetos/Playwright-Python Code/venv/Scripts/Activate.ps1"
   ```

2. Instale dependências se necessário:
   ```powershell
   pip install -r requirements.txt
   ```
   > Se não houver `requirements.txt`, instale `pytest`, `pytest-playwright`, `playwright` e `python-dotenv`.

3. Crie um arquivo `.env` na raiz com suas credenciais de teste:
   ```text
   TEST_USERNAME=Admin
   TEST_PASSWORD=admin123
   ```

4. Execute os testes:
   ```powershell
   pytest
   ```

## Observações

- O arquivo `.env` contém dados sensíveis de teste e não deve ser commitado.
- O projeto usa a fixture `credentials` em `conftest.py` para fornecer usuário e senha ao teste.
- `LoginPage` recebe as credenciais como argumentos, mantendo o teste limpo e o page object focado em interações.
