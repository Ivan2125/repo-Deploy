## FUNCIONES A UTILIZAR EN app.py

# Importaciones
import pandas as pd
import operator

# Datos a usar

reviews = pd.read_parquet("data/02-user-reviews.parquet")
gasto_items = pd.read_parquet("data/04-gasto-items.parquet")
ranking_genero = pd.read_parquet("data/05-ranking_genero.parquet")
user_time_year = pd.read_parquet("data/08-user-time-year.parquet")
items_developer = pd.read_parquet("data/07-items-developer.parquet")
piv_norm = pd.read_parquet("data/11-piv-norm.parquet")
top_dev = pd.read_parquet("data/09-top-dev.parquet")
item_similar = pd.read_parquet("data/13-item-similar.parquet")


def presentationPage():
    """
    Generates an HTML presentation page for the Steam API for video game queries.

    Returns:
    str: HTML code displaying the presentation page.
    """
    return """
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    background-color: #f4f4f4;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
                span {
                    background-color: lightgray;
                    padding: 2px 8px;
                    border-radius: 4px;
                }
                a {
                    text-decoration: none;
                    color: #3498db;
                }
                a:hover {
                    text-decoration: underline;
                }
                img {
                    vertical-align: middle;
                }
                .badge {
                    display: inline-block;
                    padding: 5px 10px;
                    font-size: 14px;
                    font-weight: bold;
                    text-align: center;
                    color: #fff;
                    background-color: #333;
                    border-radius: 4px;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <h1>API de consultas de videojuegos de la plataforma Steam</h1>
            <p>Bienvenido a la API de Steam donde puedes realizar diversas consultas sobre la plataforma de videojuegos.</p>
            <p><strong>INSTRUCCIONES:</strong></p>
            <p>Escribe <span>/docs</span> después de la URL actual para interactuar con la API.</p>
            <p>Visita mi perfil en <a href="https://www.linkedin.com/in/ivan-parra-2501//">LinkedIn <img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-blue?style=flat-square&logo=linkedin"></a></p>
            <p>El desarrollo de este proyecto se encuentra en <a href="https://github.com/Ivan2125/MLOps-Steam">GitHub <img alt="GitHub" src="https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github"></a></p>
            <div class="badge">Elaborado por Iván Parra</div>
        </body>
    </html>
    """


def developer(desarrollador):
    """
        Esta función retorna la cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.

    Args:
        def developer( desarrollador : str ):

    Returns:
        dict: {'release_year': {'cantidad_juegos': int,
                'cantidad_gratis': int,
                'porcentaje_gratis': int}}
    """
    # Filtra el dataframe por desarrollador de interés
    filtro = items_developer[items_developer["developer"] == desarrollador]
    # Calcula la cantidad de items y la cantidad de elementos gratis por año
    resumen_por_año = filtro.groupby("release_year").agg(
        cantidad_juegos=("item_id", "count"),
        cantidad_gratis=("price", lambda x: (x == 0.0).sum()),
    )

    # Calcula el porcentaje de elementos gratis por año
    resumen_por_año["porcentaje_gratis"] = (
        (resumen_por_año["cantidad_gratis"] / resumen_por_año["cantidad_juegos"] * 100)
        .fillna(0)
        .astype(int)
    )

    return resumen_por_año.to_dict(orient="index")


def userData(user_id, total_reviews=None):
    """
    Esta función devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews_recommend y cantidad de items.

    Parámetros:
    - user_id (int): Identificador único del usuario de interés.
    - total_reviews (int, opcional): Total de revisiones realizadas por todos los usuarios. Si no se proporciona,
      se calculará como la longitud de los identificadores únicos de usuarios en el conjunto de datos de revisiones.

    Devuelve:
    dict:
        - 'usuario_': Identificador único del usuario.
        - 'cantidad_dinero': Suma total de dinero gastado por el usuario en gasto_items.
        - 'porcentaje_recomendacion': Porcentaje de recomendaciones realizadas por el usuario en comparación
          con el total de revisiones en el conjunto de datos.
        - 'total_items': La cantidad máxima de items comprados por el usuario en gasto_items.
    """
    # Filtra por el usuario de interés en gasto_items
    usuario_gastos = gasto_items[gasto_items["user_id"] == user_id]

    # Calcula la cantidad de dinero gastado y el total de items para el usuario de interés

    cantidad_dinero = usuario_gastos["price"].sum()
    count_items = usuario_gastos["items_count"].max()

    # Calcula el total de recomendaciones realizadas por el usuario de interés
    total_recomendaciones = reviews[reviews["user_id"] == user_id][
        "reviews_recommend"
    ].sum()

    # Calcula el porcentaje de recomendaciones realizadas por el usuario de interés
    if total_reviews is None:
        total_reviews = len(reviews["user_id"].unique())

    porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100

    return {
        "usuario_": user_id,
        "cantidad_dinero": cantidad_dinero,
        "porcentaje_recomendacion": round(porcentaje_recomendaciones, 2),
        "total_items": count_items,
    }


def userForGenre(genero, usuario_especifico=None):
    """
    Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

    Parámetros:
    - df (DataFrame): DataFrame que contiene las columnas 'playtime_forever', 'user_id', 'genres', 'release_year'.
    - genero (str): Género específico para el cual se desea obtener la información.
    - usuario_especifico (str, opcional): Usuario específico para el cual se calculará la acumulación de horas jugadas. Si no se proporciona, se usará el usuario con más horas jugadas.

    Retorna:
    dict: Un diccionario con la siguiente estructura:
        {
            "Usuario con más horas jugadas para <genero>": <usuario>,
            "Horas jugadas": [
                {"Año": <año1>, "Horas": <horas1>},
                {"Año": <año2>, "Horas": <horas2>},
                ...
            ]
        }
    """

    # Filtra el DataFrame por el género dado
    data_genero = user_time_year[
        user_time_year["genres"].str.contains(genero, case=False, na=False)
    ]

    if usuario_especifico is None:
        # Encuentra el usuario con más horas jugadas para el género dado
        usuario_mas_horas = (
            data_genero.groupby("user_id")["playtime_forever"].sum().idxmax()
        )
    else:
        usuario_mas_horas = usuario_especifico

    # Filtra nuevamente por el usuario con más horas jugadas
    data_genero_usuario = data_genero[data_genero["user_id"] == usuario_mas_horas]

    # Calcula la acumulación de horas jugadas por año de lanzamiento
    horas_por_año = (
        data_genero_usuario.groupby("release_year")["playtime_forever"]
        .sum()
        .reset_index()
    )

    # Formatea el resultado como un diccionario
    resultado = {
        "Usuario con más horas jugadas para {}: {}".format(
            genero, usuario_mas_horas
        ): usuario_mas_horas,
        "Horas jugadas": [
            {"Año": int(año), "Horas": int(horas)}
            for año, horas in zip(
                horas_por_año["release_year"], horas_por_año["playtime_forever"]
            )
        ],
    }

    return resultado


def usersRecommend(anio):
    """
    Devuelve el top 3 de desarrolladores con juegos MÁS recomendados y análisis de sentimientos positivos (2) por usuarios para el año dado.

    Parámetros:
    - año (int): Año específico para el cual se desea obtener la información.

    Retorna:
    list: Una lista de diccionarios con el siguiente formato:
        [
            {"Puesto 1": <desarrollador1>, "recomendaciones": <cantidad1>},
            {"Puesto 2": <desarrollador2>, "recomendaciones": <cantidad2>},
            {"Puesto 3": <desarrollador3>, "recomendaciones": <cantidad3>}
        ]
    """
    # Filtramos por el año deseado
    df_filtered = top_dev[top_dev["release_year"] == anio]

    # Filtramos por comentarios recomendados y sentiment_analysis positivo/neutral
    df_filtered = df_filtered[
        (df_filtered["reviews_recommend"] == True)
        & (df_filtered["sentiment_analysis"].isin([2]))
    ]

    # Obtenemos el top 3 de juegos recomendados
    top_games = df_filtered["developer"].value_counts().head(3).reset_index()

    # Modificamos la estructura del resultado
    result = [
        {"Puesto {}".format(i + 1): juego, "recomendaciones": count}
        for i, (juego, count) in enumerate(
            zip(top_games["developer"], top_games["count"])
        )
    ]

    return result


def developerReviewsAnalysis(desarrollador):
    """
    Analiza las reseñas de usuarios para un desarrollador específico y devuelve un diccionario con la cantidad total de registros de reseñas categorizados con un análisis de sentimiento como positivo o negativo.

    Parámetros:
    - df (DataFrame): DataFrame que contiene las columnas 'playtime_forever', 'user_id', 'item_id', 'genres', 'release_year'.
    - desarrollador (str): Nombre del desarrollador para el cual se desea realizar el análisis.

    Retorna:
    dict: Un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de
    reseñas categorizados con un análisis de sentimiento como valor positivo o negativo.
    """
    # Filtra el DataFrame por el desarrollador deseado
    df_desarrollador = top_dev[top_dev["developer"] == desarrollador]

    # Cuenta la cantidad total de registros de reseñas categorizados como positivos o negativos
    count_sentimiento = df_desarrollador["sentiment_analysis"].value_counts()

    # Formatea el resultado como un diccionario
    result = {
        desarrollador: {
            "Negative": count_sentimiento.get(0, 0),
            "Positive": count_sentimiento.get(2, 0),
        }
    }

    return result


def recomendacionJuego(game):
    """
    Muestra una lista de juegos similares a un juego dado.

    Args:
        game (str): El nombre del juego para el cual se desean encontrar juegos similares.

    Returns:
        None: Un diccionario con 5 nombres de juegos recomendados.

    """
    # Obtener la lista de juegos similares ordenados
    similar_games = item_similar.sort_values(by=game, ascending=False).iloc[1:6]

    count = 1
    contador = 1
    recomendaciones = {}

    for item in similar_games:
        if contador <= 5:
            item = str(item)
            recomendaciones[count] = item
            count += 1
            contador += 1
        else:
            break
    return recomendaciones
