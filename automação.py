from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pyautogui
import pyperclip
import re


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # mantém aberto

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www45.bb.com.br/fmc/frm/fw0707314_1.jsp")
sleep(5)
pyautogui.click(306, 29)
sleep(2)

# abrir planilha
link = "https://docs.google.com/spreadsheets/d/1yvNzH--TsgQmk8j3IvxRsxDvQ6jbkhNAu4Ym1xArIus/edit?gid=1662462019#gid=1662462019"
pyperclip.copy(link)
pyautogui.hotkey("ctrl", "v")
sleep(3)
pyautogui.press("enter")

# copiar valor da A6
sleep(5)
pyautogui.click(241, 433)   # célula A6
sleep(3)
pyautogui.hotkey("ctrl", "c")
sleep(3)

# pegar texto copiado
autor = pyperclip.paste().strip()
print("Autor copiado ->", autor)
sleep(3)

# preencher nome
campo_nome = driver.find_element(By.NAME, "nome")
campo_nome.clear()
campo_nome.send_keys(autor)

# ===============================
#   LÓGICA CONDICIONAL PARA CNPJ
# ===============================

# dicionário de regras
regras_cnpj = {
    "BEZERRA & QUEIROZ LTDA": "12.345.678/0001-99",
    "EDITORA NAPOLEÃO LTDA": "06.228.693/0001-50",
    
}

# pega CNPJ conforme nome
cnpj_preencher = regras_cnpj.get(autor, "")

print("CNPJ a preencher ->", cnpj_preencher)

# preencher CNPJ no campo correspondente
campo_cnpj = driver.find_element(By.ID, "cnpj")
campo_cnpj.clear()
campo_cnpj.send_keys(cnpj_preencher)

sleep(3)

# Preencher numero do processo
pyautogui.click(170, 345)
pyautogui.hotkey("ctrl", "c")
sleep(3)




# pegar o número copiado
numero_processo = pyperclip.paste().strip()

# limpar o número removendo tudo que não for dígito
numero_limpo = re.sub(r"\D", "", numero_processo)

print("Número limpo ->", numero_limpo)

# preencher no input correto
campo_processo = driver.find_element(By.ID, "num_processo")
campo_processo.clear()
campo_processo.send_keys(numero_limpo)

# preencher Unidade
sleep(3)
pyautogui.click(655, 500)   # CLICA NA PLANILHA PARA COPIAR C9
sleep(1)
pyautogui.hotkey("ctrl", "c")
sleep(1)

# pega texto copiado
valor_unidade = pyperclip.paste().strip()
print("Unidade copiada ->", valor_unidade)

# preenche no campo da página
campo_unidade = driver.find_element(By.NAME, "unidade")
campo_unidade.clear()
campo_unidade.send_keys(valor_unidade)


# pegar valor na planilha (clicando na célula certa)
sleep(4)
pyautogui.click(688, 434)   # célula onde está o VALOR
sleep(1)
pyautogui.hotkey("ctrl", "c")
sleep(1)

# ler valor copiado
valor_copiado = pyperclip.paste().strip()
print("Valor copiado ->", valor_copiado)

# preencher no campo de valor do formulário
campo_valor = driver.find_element(By.ID, "valor")
campo_valor.clear()

# enviar caractere por caractere (evita problemas com máscara)
for c in valor_copiado:
    campo_valor.send_keys(c)
    sleep(0.05)

# pegar da planilha
sleep(2)
pyautogui.click(827, 498)   # célula da planilha com a descrição
sleep(1)
pyautogui.hotkey("ctrl", "c")
sleep(1)

descricao = pyperclip.paste().strip()
print("Descrição copiada ->", descricao)

# preencher no textarea da página
campo_descricao = driver.find_element(By.NAME, "area1")
campo_descricao.clear()
campo_descricao.send_keys(descricao)

#preencher numero da guia
# pegar da planilha
sleep(2)
pyautogui.click(802, 431)
sleep(2)
pyautogui.hotkey("ctrl", "c")
sleep(2)

# pegar código real
codigo = pyperclip.paste().strip()
codigo = codigo.replace("–", "-").replace("—", "-")
codigo = re.sub(r"[^0-9\-]", "", codigo)
print("Código final ->", repr(codigo))

# abrir dropdown
pyautogui.click(126, 28)
sleep(5)
pyautogui.click(786, 393)
sleep(2)

if codigo == "434-1":
    pyautogui.click(596, 762)
elif codigo == "120-1":
    pyautogui.click(243, 375)
elif codigo == "206-2":
    pyautogui.click(231, 754)
else:
    print("Código não mapeado!")


if codigo == "434-1":
    pyautogui.click(596, 762)   # posição do código 201-0
elif codigo == "120-1":
    pyautogui.click(243, 375)   # posição do código 120-1
elif codigo == "206-2": 
    pyautogui.click(231, 754)   # posição do código 140-6
else:
    print("Código não mapeado!")

# (se quiser pode remover essa parte)

search = driver.find_element(By.NAME, "q")
search.send_keys("ChatGPT")
search.send_keys(Keys.RETURN)


print(driver.title)

