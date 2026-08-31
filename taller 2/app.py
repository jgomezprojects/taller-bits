import os
import flet as ft


# ============================================================
# CONFIGURACIÓN DEL PROYECTO
# ============================================================

FILAS = 8
COLUMNAS = 8
TOTAL_BITS = FILAS * COLUMNAS
TAMANO_CELDA = 44
ESPACIADO = 5


# ============================================================
# COLORES
# ============================================================

BG = "#0A0F0D"
PANEL = "#111A17"
PANEL_BORDE = "#1F332B"

PIXEL_APAGADO = "#16211D"
PIXEL_HOVER = "#223A31"
PIXEL_ENCENDIDO = "#39FF6A"

ACENTO = "#39FF6A"
ACENTO_SECUNDARIO = "#FFB020"

TEXTO = "#EAF7F0"
TEXTO_TENUE = "#5C7A6E"
ERROR = "#FF5C5C"


# ============================================================
# FUENTE
# ============================================================

FUENTE_MONO = "Space Mono"


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main(page: ft.Page):

    # --------------------------------------------------------
    # CONFIGURACIÓN DE LA VENTANA
    # --------------------------------------------------------

    page.fonts = {
        FUENTE_MONO:
            "https://raw.githubusercontent.com/google/fonts/master/ofl/spacemono/SpaceMono-Regular.ttf",

        FUENTE_MONO + " Bold":
            "https://raw.githubusercontent.com/google/fonts/master/ofl/spacemono/SpaceMono-Bold.ttf",
    }

    page.title = "Editor de Sprites 8x8"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG

    page.window.width = 640
    page.window.height = 900
    page.window.resizable = False

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO

    page.theme = ft.Theme(
        font_family=FUENTE_MONO
    )


    # ========================================================
    # LISTA DE LOS 64 PÍXELES
    # ========================================================

    botones = []


    # ========================================================
    # CONVERSIÓN MATRIZ → BINARIO
    # ========================================================

    def leer_matriz_a_binario():

        bits = []

        for celda in botones:

            if celda.bgcolor == PIXEL_ENCENDIDO:
                bits.append("1")
            else:
                bits.append("0")

        return "".join(bits)


    # ========================================================
    # CONVERSIÓN BINARIO → HEX
    # ========================================================

    def binario_a_hex(cadena_binaria):

        numero = int(cadena_binaria, 2)

        # 16 caracteres HEX = 64 bits
        return format(numero, "016X")


    # ========================================================
    # CONVERSIÓN HEX → BINARIO
    # ========================================================

    def hex_a_binario_64(texto_hex):

        numero = int(texto_hex, 16)

        # Siempre exactamente 64 bits
        return format(numero, "064b")


    # ========================================================
    # ACTUALIZAR REGISTRO
    # ========================================================

    def actualizar_registro_desde_pantalla():

        binario = leer_matriz_a_binario()

        texto_hex_actual.value = binario_a_hex(binario)

        bits_activos = binario.count("1")

        contador_bits.value = (
            f"BITS ACTIVOS: {bits_activos:02d} / {TOTAL_BITS}"
        )

        page.update()


    # ========================================================
    # EVENTO: MOUSE ENTRA
    # ========================================================

    def al_entrar_mouse(e):

        if e.control.bgcolor == PIXEL_APAGADO:

            e.control.bgcolor = PIXEL_HOVER
            e.control.update()


    # ========================================================
    # EVENTO: MOUSE SALE
    # ========================================================

    def al_salir_mouse(e):

        if e.control.bgcolor == PIXEL_HOVER:

            e.control.bgcolor = PIXEL_APAGADO
            e.control.update()


    # ========================================================
    # EVENTO: CLIC EN UN PÍXEL
    # ========================================================

    def alternar_pixel(e):

        celda = e.control

        if celda.bgcolor in (
            PIXEL_APAGADO,
            PIXEL_HOVER
        ):

            celda.bgcolor = PIXEL_ENCENDIDO

        else:

            celda.bgcolor = PIXEL_APAGADO

        actualizar_registro_desde_pantalla()


    # ========================================================
    # CREACIÓN DE LA MATRIZ 8x8
    # ========================================================

    grid = ft.GridView(

        expand=False,

        width=(
            TAMANO_CELDA * COLUMNAS
            + (COLUMNAS - 1) * ESPACIADO
        ),

        height=(
            TAMANO_CELDA * FILAS
            + (FILAS - 1) * ESPACIADO
        ),

        runs_count=COLUMNAS,

        max_extent=TAMANO_CELDA,

        child_aspect_ratio=1,

        spacing=ESPACIADO,

        run_spacing=ESPACIADO,
    )


    # ========================================================
    # CREAR LOS 64 PÍXELES
    # ========================================================

    for fila in range(FILAS):

        for columna in range(COLUMNAS):

            celda = ft.Container(

                bgcolor=PIXEL_APAGADO,

                border_radius=4,

                border=ft.Border.all(
                    1,
                    PANEL_BORDE
                ),

                ink=True,

                animate=150,

                on_click=alternar_pixel,
            )


            def controlar_hover(e):

                if e.data == "true":
                    al_entrar_mouse(e)
                else:
                    al_salir_mouse(e)


            celda.on_hover = controlar_hover

            botones.append(celda)

            grid.controls.append(celda)


    # ========================================================
    # ETIQUETA DE PANEL
    # ========================================================

    def etiqueta_panel(texto):

        return ft.Row(

            spacing=6,

            controls=[

                ft.Text(
                    ">",
                    color=ACENTO,
                    size=13,
                    font_family=FUENTE_MONO + " Bold",
                ),

                ft.Text(
                    texto,
                    size=12,
                    color=TEXTO_TENUE,
                    font_family=FUENTE_MONO + " Bold",
                ),
            ],
        )


    # ========================================================
    # PANEL DEL FRAMEBUFFER
    # ========================================================

    panel_grid = ft.Container(

        content=ft.Column(

            spacing=10,

            horizontal_alignment=
                ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Row(

                    alignment=
                        ft.MainAxisAlignment.SPACE_BETWEEN,

                    controls=[
                        etiqueta_panel(
                            "FRAMEBUFFER 8x8"
                        )
                    ],
                ),

                grid,
            ],
        ),

        bgcolor=PANEL,

        border=ft.Border.all(
            1,
            PANEL_BORDE
        ),

        border_radius=10,

        padding=18,
    )


    # ========================================================
    # TEXTO DEL REGISTRO HEX
    # ========================================================

    texto_hex_actual = ft.Text(

        value="0" * 16,

        size=30,

        weight=ft.FontWeight.BOLD,

        font_family=FUENTE_MONO + " Bold",

        color=ACENTO,

        selectable=True,
    )


    # ========================================================
    # CONTADOR DE BITS
    # ========================================================

    contador_bits = ft.Text(

        value="BITS ACTIVOS: 00 / 64",

        size=11,

        color=TEXTO_TENUE,

        font_family=FUENTE_MONO,
    )


    # ========================================================
    # PANEL DEL REGISTRO
    # ========================================================

    panel_registro = ft.Container(

        content=ft.Column(

            spacing=8,

            horizontal_alignment=
                ft.CrossAxisAlignment.CENTER,

            controls=[

                etiqueta_panel(
                    "REGISTRO HEX (64 bits)"
                ),

                ft.Container(

                    content=texto_hex_actual,

                    bgcolor="#081310",

                    border=ft.Border.all(
                        1,
                        PANEL_BORDE
                    ),

                    border_radius=6,

                    padding=ft.Padding.symmetric(
                        vertical=14,
                        horizontal=18
                    ),

                    width=520,

                    alignment=ft.Alignment.CENTER,
                ),

                contador_bits,
            ],
        ),

        bgcolor=PANEL,

        border=ft.Border.all(
            1,
            PANEL_BORDE
        ),

        border_radius=10,

        padding=18,
    )


    # ========================================================
    # VALIDACIÓN HEX
    # ========================================================

    DIGITOS_HEX_VALIDOS = set(
        "0123456789ABCDEF"
    )


    def validar_hex(texto):

        # La guía establece máximo 16 caracteres
        if len(texto) == 0:
            return False

        if len(texto) > 16:
            return False

        return all(
            caracter in DIGITOS_HEX_VALIDOS
            for caracter in texto.upper()
        )


    # ========================================================
    # CAMPO DE ENTRADA HEX
    # ========================================================

    campo_hex = ft.TextField(

        label="CODIGO HEXADECIMAL (16 DIGITOS)",

        label_style=ft.TextStyle(
            size=11,
            color=TEXTO_TENUE,
            font_family=FUENTE_MONO
        ),

        hint_text="1A2B3C4D5E6F0000",

        hint_style=ft.TextStyle(
            color="#3A4F45"
        ),

        max_length=16,

        capitalization=
            ft.TextCapitalization.CHARACTERS,

        text_style=ft.TextStyle(
            font_family=FUENTE_MONO,
            color=ACENTO
        ),

        border_color=PANEL_BORDE,

        focused_border_color=ACENTO,

        border_radius=6,

        filled=True,

        bgcolor="#081310",

        cursor_color=ACENTO,

        counter_style=ft.TextStyle(
            color=TEXTO_TENUE,
            size=10
        ),
    )


    # ========================================================
    # MENSAJE DE ERROR
    # ========================================================

    mensaje_error = ft.Text(

        value="",

        color=ERROR,

        size=12,

        font_family=FUENTE_MONO,
    )


    # ========================================================
    # CARGAR HEX EN LA MATRIZ
    # ========================================================

    def cargar_hex_en_pantalla(e):

        texto = (
            campo_hex.value.strip().upper()
            if campo_hex.value
            else ""
        )


        # -----------------------------
        # VALIDAR
        # -----------------------------

        if not validar_hex(texto):

            if len(texto) == 0:

                mensaje_error.value = (
                    "ERROR: introduce un código hexadecimal."
                )

            elif len(texto) > 16:

                mensaje_error.value = (
                    "ERROR: máximo 16 caracteres."
                )

            else:

                mensaje_error.value = (
                    "ERROR: usa solo 0-9 y A-F."
                )

            page.update()

            return


        # -----------------------------
        # LIMPIAR ERROR
        # -----------------------------

        mensaje_error.value = ""


        # -----------------------------
        # HEX → BINARIO
        # -----------------------------

        binario = hex_a_binario_64(texto)


        # -----------------------------
        # BINARIO → MATRIZ
        # -----------------------------

        for celda, bit in zip(
            botones,
            binario
        ):

            if bit == "1":

                celda.bgcolor = PIXEL_ENCENDIDO

            else:

                celda.bgcolor = PIXEL_APAGADO


        # -----------------------------
        # ACTUALIZAR INTERFAZ
        # -----------------------------

        actualizar_registro_desde_pantalla()


    # ========================================================
    # LIMPIAR TODO
    # ========================================================

    def limpiar_todo(e):

        for celda in botones:

            celda.bgcolor = PIXEL_APAGADO


        campo_hex.value = ""

        mensaje_error.value = ""


        actualizar_registro_desde_pantalla()


    # ========================================================
    # BOTÓN CARGAR HEX
    # ========================================================

    boton_cargar = ft.FilledButton(

        content="CARGAR HEX",

        icon=ft.Icons.BOLT_ROUNDED,

        on_click=cargar_hex_en_pantalla,

        style=ft.ButtonStyle(

            bgcolor=ACENTO_SECUNDARIO,

            color="#141414",

            text_style=ft.TextStyle(
                font_family=FUENTE_MONO + " Bold",
                size=13
            ),

            shape=ft.RoundedRectangleBorder(
                radius=6
            ),

            padding=18,
        ),
    )


    # ========================================================
    # BOTÓN LIMPIAR
    # ========================================================

    boton_limpiar = ft.OutlinedButton(

        content="LIMPIAR",

        icon=ft.Icons.CLEAR_ROUNDED,

        on_click=limpiar_todo,

        style=ft.ButtonStyle(

            side=ft.BorderSide(
                1,
                PANEL_BORDE
            ),

            color=TEXTO_TENUE,

            text_style=ft.TextStyle(
                font_family=FUENTE_MONO + " Bold",
                size=13
            ),

            shape=ft.RoundedRectangleBorder(
                radius=6
            ),

            padding=18,
        ),
    )


    # ========================================================
    # PANEL DE ENTRADA
    # ========================================================

    panel_entrada = ft.Container(

        content=ft.Column(

            spacing=12,

            controls=[

                etiqueta_panel(
                    "CARGAR REGISTRO EXTERNO"
                ),

                campo_hex,

                mensaje_error,

                ft.Row(

                    alignment=
                        ft.MainAxisAlignment.END,

                    spacing=10,

                    controls=[
                        boton_limpiar,
                        boton_cargar
                    ],
                ),
            ],
        ),

        bgcolor=PANEL,

        border=ft.Border.all(
            1,
            PANEL_BORDE
        ),

        border_radius=10,

        padding=18,
    )


    # ========================================================
    # ENCABEZADO
    # ========================================================

    encabezado = ft.Column(

        spacing=4,

        horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,

        controls=[

            ft.Row(

                alignment=
                    ft.MainAxisAlignment.CENTER,

                spacing=8,

                controls=[

                    ft.Text(

                        "EDITOR DE SPRITES 8x8",

                        size=22,

                        weight=ft.FontWeight.BOLD,

                        color=TEXTO,

                        font_family=
                            FUENTE_MONO + " Bold",
                    ),
                ],
            ),

            ft.Container(

                width=520,

                height=2,

                bgcolor=ACENTO,

                opacity=0.5,

                border_radius=2,

                margin=ft.Margin.only(
                    top=8
                ),
            ),
        ],
    )


    # ========================================================
    # CONSTRUIR INTERFAZ
    # ========================================================

    page.add(

        ft.Container(

            padding=ft.Padding.only(

                top=34,
                bottom=34,
                left=24,
                right=24,
            ),

            content=ft.Column(

                horizontal_alignment=
                    ft.CrossAxisAlignment.CENTER,

                spacing=18,

                controls=[

                    encabezado,

                    panel_grid,

                    panel_registro,

                    panel_entrada,
                ],
            ),
        )
    )


    # ========================================================
    # ESTADO INICIAL
    # ========================================================

    actualizar_registro_desde_pantalla()


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    ft.run(

        main,

        view=ft.AppView.WEB_BROWSER,

        port=int(
            os.environ.get(
                "PORT",
                8550
            )
        ),
    )