# Importaciones
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import funciones as af

import importlib

importlib.reload(af)

# Se instancia la aplicación
app = FastAPI()


# Funciones
@app.get(path="/", response_class=HTMLResponse, tags=["Home"])
def presentationPage():
    """
    Página de inicio que muestra una presentación.

    Returns:
    HTMLResponse: Respuesta HTML que muestra la presentación.
    """
    return af.presentationPage()


@app.get(
    path="/developer",
    description=""" <font color="green">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el Desarrollador en la caja de abajo.<br>
                        3. Scrollear a "Resposes" para ver la cantidad de items y porcentaje de contenido Free por año según empresa de desarrollo.
                        </font>
                        """,
    tags=["Consultas Generales"],
)
def developer(
    desarrollador: str = Query(
        ..., description="Nombre del Desarrollador", example="Valve"
    )
):

    return af.developer(desarrollador)


@app.get(
    path="/userData",
    description=""" <font color="green">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese un user_id<br>
                        3. Scrollear a "Resposes" para ver la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews_recommend y cantidad de items.</font>
                        """,
    tags=["Consultas Generales"],
)
def userData(user_id: str = Query(..., description="user_id", example="evcentric")):
    return af.userdata(user_id)


@app.get(
    path="/userForGenre",
    description=""" <font color="green">
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el género del juego en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.
                        </font>
                        """,
    tags=["Consultas Generales"],
)
def userForGenre(genero: str = Query(..., description="Género", example="Indie")):
    return af.genre(genero)


@app.get(
    path="/usersRecommend",
    description=""" <font color="green">
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el género en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver el top 3 de desarrolladores con juegos MÁS recomendados y análisis de sentimientos positivos (2) por usuarios para el año dado.
                        </font>
                        """,
    tags=["Consultas Generales"],
)
def usersRecommend(anio: str = Query(..., description="Año", example="2012")):
    return af.usersRecommend(anio)


@app.get(
    path="/developerReviewsAnalysis",
    description=""" <font color="green">
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el nombre del desarrollador en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver la cantidad total de registros de reseñas categorizados con un análisis de sentimiento como positivo o negativo del desarrollador.
                        </font>
                        """,
    tags=["Consultas Generales"],
)
def developerReviewsAnalysis(
    desarrollador: str = Query(
        ..., description="Desarrollador del videojuego", example="Valve"
    )
):
    return af.developerReviewsAnalysis(desarrollador)


@app.get(
    "/recomendacionJuego",
    description=""" <font color="green">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese el nombre de un juego en box abajo.<br>
                    3. Scrollear a "Resposes" para ver los 5 juegos recomendados.
                    </font>
                    """,
    tags=["Recomendación"],
)
def recomendacionJuego(
    game: str = Query(
        ...,
        description="Juego a partir del cuál se hace la recomendación de otros juego",
        example="Counter-Strike",
    )
):
    return af.recomendacionJuego(game)
