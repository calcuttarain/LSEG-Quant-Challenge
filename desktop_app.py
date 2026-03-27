import sys
import re
import ollama
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QSplitter)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QThread, Signal, Qt

SYSTEM_PROMPT = """Ești un expert în arhitectură software și diagrame logice.
Transformă cerința utilizatorului într-o diagramă Mermaid.js.
Răspunde STRICT cu codul Mermaid încadrat de tag-urile ```mermaid și ```.
Fără niciun alt text explicativ."""

# --- Thread pentru rularea LLM-ului în fundal ---
class GeneratorThread(QThread):
    finished_signal = Signal(str, str) # PySide6 folosește 'Signal'

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        print("Thread: Încep generarea cu Ollama...")
        try:
            response = ollama.chat(model='llama3', messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': self.prompt}
            ])
            
            llm_output = response['message']['content']
            match = re.search(r'```mermaid\n(.*?)```', llm_output, re.DOTALL)
            
            if match:
                print("Thread: Diagramă generată cu succes.")
                self.finished_signal.emit(match.group(1).strip(), "")
            else:
                print("Thread: Eroare de formatare (nu am găsit tag-ul mermaid).")
                self.finished_signal.emit("", f"Eroare formatare:\n{llm_output}")
        except Exception as e:
            print(f"Thread: Eroare la conexiunea cu Ollama: {e}")
            self.finished_signal.emit("", f"Eroare Ollama: {str(e)}")


# --- Fereastra Principală a Aplicației ---
class DiagramApp(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Inițializare fereastră...")
        self.setWindowTitle("Generare Diagrame Local (Ollama + PySide6)")
        self.resize(1000, 700)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Panoul Stânga (Chat)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        left_layout.addWidget(self.chat_history)

        input_layout = QHBoxLayout()
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Scrie aici fluxul diagramei...")
        self.prompt_input.returnPressed.connect(self.generate_diagram)
        
        self.send_btn = QPushButton("Trimite")
        self.send_btn.clicked.connect(self.generate_diagram)
        
        input_layout.addWidget(self.prompt_input)
        input_layout.addWidget(self.send_btn)
        left_layout.addLayout(input_layout)

        # Panoul Dreapta (Diagrama)
        print("Inițializare WebEngine...")
        self.diagram_view = QWebEngineView()
        self.set_empty_diagram()

        splitter.addWidget(left_panel)
        splitter.addWidget(self.diagram_view)
        splitter.setSizes([400, 600])
        print("Interfață încărcată!")

    def set_empty_diagram(self):
        self.diagram_view.setHtml("<html><body><h3 style='font-family:sans-serif; color:gray; text-align:center; margin-top:50px;'>Diagrama va apărea aici</h3></body></html>")

    def generate_diagram(self):
        user_text = self.prompt_input.text().strip()
        if not user_text:
            return

        self.chat_history.append(f"<b>Tu:</b> {user_text}")
        self.prompt_input.clear()
        self.send_btn.setEnabled(False)
        self.chat_history.append("<i>Generez diagrama... te rog așteaptă.</i><br>")
        
        self.thread = GeneratorThread(user_text)
        self.thread.finished_signal.connect(self.on_generation_finished)
        self.thread.start()

    def on_generation_finished(self, mermaid_code, error):
        self.send_btn.setEnabled(True)
        
        if error:
            self.chat_history.append(f"<b style='color:red;'>Eroare:</b> {error}<br><br>")
            return

        self.chat_history.append("<b style='color:green;'>Sistem:</b> Diagramă generată cu succes!<br><br>")
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
            </script>
        </head>
        <body style="background-color: white; margin: 0; padding: 20px;">
            <div class="mermaid">
                {mermaid_code}
            </div>
        </body>
        </html>
        """
        self.diagram_view.setHtml(html_content)

if __name__ == '__main__':
    print("Pornire aplicație...")
    app = QApplication(sys.argv)
    window = DiagramApp()
    window.show()
    sys.exit(app.exec())