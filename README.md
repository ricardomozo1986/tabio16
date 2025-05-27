# Plataforma Predial en Streamlit (Despliegue Render)

## ¿Qué hace esta app?
- Analiza cumplimiento tributario, morosidad, avalúos y recaudo predial.
- Muestra mapas, tablas interactivas y simulaciones.
- Ideal para gestión pública territorial.

## ¿Cómo desplegar en Render?
1. Sube este repositorio a tu cuenta de GitHub.
2. Ve a [https://dashboard.render.com](https://dashboard.render.com) > New Web Service.
3. Conecta tu cuenta de GitHub y selecciona este repositorio.
4. Configura:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app_streamlit_predial_FINAL_OK.py --server.port=10000`
5. Crea el servicio y espera 1–2 minutos.

