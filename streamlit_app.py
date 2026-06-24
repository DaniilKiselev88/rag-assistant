import requests
import streamlit as st
import json

# Используйте правильный URL в зависимости от окружения
# Для Docker: "http://backend:8000/rag"
# Для локальной разработки: "http://localhost:8000/rag"
API_URL = "http://backend:8000/rag"

st.set_page_config(page_title="RAG Assistant", page_icon="📄", layout="wide")

st.title("📄 RAG Assistant")
st.write("Загрузите PDF и задайте вопрос по документам.")

# ========================
# Sidebar: Upload PDF
# ========================

with st.sidebar:
    st.header("Загрузка документа")

    uploaded_file = st.file_uploader(
        "Выберите PDF-файл",
        type=["pdf"]
    )

    if uploaded_file is not None:
        if st.button("Загрузить PDF"):
            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        "application/pdf"
                    )
                }

                response = requests.post(
                    f"{API_URL}/upload",
                    files=files,
                    timeout=300
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success(
                        f"✅ Файл успешно обработан. "
                        f"Создано чанков: {data.get('chunks_count', 0)}"
                    )
                else:
                    error_msg = "Ошибка загрузки"
                    try:
                        error_data = response.json()
                        error_msg = error_data.get("detail", error_msg)
                    except:
                        error_msg = response.text or error_msg
                    st.error(f"❌ {error_msg}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Не удалось подключиться к серверу. Проверьте, запущен ли бэкенд.")
            except requests.exceptions.Timeout:
                st.error("❌ Таймаут соединения. Сервер не отвечает.")
            except Exception as e:
                st.error(f"❌ Ошибка: {str(e)}")

# ========================
# Main Area: Ask Question
# ========================

st.subheader("Задайте вопрос")

question = st.text_area(
    "Введите вопрос",
    height=120,
    placeholder="Например: Что такое FastAPI?"
)

if st.button("Отправить", type="primary"):
    if not question.strip():
        st.warning("⚠️ Введите вопрос.")
    else:
        try:
            with st.spinner("🔍 Поиск ответа..."):
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question},
                    timeout=300
                )

            if response.status_code == 200:
                result = response.json()
                st.markdown("### 💡 Ответ")
                st.write(result.get("answer", "Не удалось получить ответ"))
                
                sources = result.get("sources", [])
                if sources:
                    with st.expander(f"📚 Источники ({len(sources)})"):
                        for source in sources:
                            st.markdown(f"- {source}")
            else:
                error_msg = "Ошибка запроса"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", error_msg)
                except:
                    error_msg = response.text or error_msg
                st.error(f"❌ {error_msg}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Не удалось подключиться к серверу. Проверьте, запущен ли бэкенд.")
        except requests.exceptions.Timeout:
            st.error("❌ Таймаут соединения. Сервер не отвечает.")
        except Exception as e:
            st.error(f"❌ Ошибка: {str(e)}")