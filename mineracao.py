import sys
import requests
from PyQt5 import QtWidgets, uic
from bs4 import BeautifulSoup

class WebScraperApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(WebScraperApp, self).__init__()
        uic.loadUi('interface.ui', self)

        self.urlInput = self.findChild(QtWidgets.QLineEdit, 'urlInput')
        self.executeButton = self.findChild(QtWidgets.QPushButton, 'executeButton')
        self.resultDisplay = self.findChild(QtWidgets.QTextEdit, 'resultDisplay')
        self.statusLabel = self.findChild(QtWidgets.QLabel, 'statusLabel')
        self.dataSelector = self.findChild(QtWidgets.QComboBox, 'dataSelector')

        self.executeButton.clicked.connect(self.execute_scraping)

    def execute_scraping(self):
        url = self.urlInput.text()
        if not url:
            self.statusLabel.setText("Por favor, insira um URL.")
            return

        self.statusLabel.setText("Iniciando pesquisa...")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.content
                soup = BeautifulSoup(content, 'html.parser')
                result = ""

                data_type = self.dataSelector.currentText()
                if data_type == "Títulos":
                    titles = soup.find_all('h1')
                    result = "\n".join([title.get_text() for title in titles])

                elif data_type == "Links":
                    links = soup.find_all('a', href=True)
                    result = "\n".join([link['href'] for link in links])

                elif data_type == "Imagens":
                    images = soup.find_all('img', src=True)
                    result = "\n".join([img['src'] for img in images])

                elif data_type == "Parágrafos":
                    paragraphs = soup.find_all('p')
                    result = "\n".join([p.get_text() for p in paragraphs])

                elif data_type == "Cabeçalhos":
                    headers = soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])
                    result = "\n".join([header.get_text() for header in headers])

                elif data_type == "Listas":
                    lists = soup.find_all(['ul', 'ol'])
                    result = "\n".join([lst.get_text() for lst in lists])

                elif data_type == "Tabelas":
                    tables = soup.find_all('table')
                    result = "\n".join([table.get_text() for table in tables])

                elif data_type == "Metadados":
                    metas = soup.find_all('meta')
                    result = "\n".join([str(meta) for meta in metas])

                elif data_type == "Scripts":
                    scripts = soup.find_all('script')
                    result = "\n".join([script.get_text() for script in scripts])

                elif data_type == "Comentários":
                    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                    result = "\n".join([comment for comment in comments])

                self.resultDisplay.setPlainText(result if result else "Nenhum dado encontrado.")
                self.statusLabel.setText("Pesquisa concluída.")
            else:
                self.statusLabel.setText(f"Erro na requisição: {response.status_code}")
        except Exception as e:
            self.statusLabel.setText(f"Erro: {str(e)}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = WebScraperApp()
    window.show()
    sys.exit(app.exec_())
