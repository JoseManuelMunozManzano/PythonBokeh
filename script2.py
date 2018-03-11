from flask import Flask, render_template
# Returning html templates
# Se usa el método render template del framework flask
# Lo que hace es acceder a un fichero HTML almacenado en algún sitio de nuestra aplicación Python,
# de nuestros ficheros Python, y render_template muestra ese HTML del URL requerido

app = Flask(__name__)


# Se añade la página HTML
# Y dicha página deberá existir en una carpeta llamada templates que se encuentre en el mismo directorio
# que nuestra aplicación Python
# Los CSS se debe añadr a una carpeta llamada static. Dentro de static se ha creado otra carpeta llamada css
# Si fueran imágenes se crearía dentro de static la carpeta images
@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about/')
def about():
    return render_template("about.html")


@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime(2015, 11, 1)
    end = datetime.datetime(2016, 3, 10)

    df = data.DataReader(name="GOOG", data_source="google", start=start, end=end)

    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Close - df.Open)
    differ = df.Close - df.Open
    df['color'] = ['#CCFFFF' if x > 0 else '#FF3333' for x in differ]

    p = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode='scale_width')
    p.title.text = "Candlestick Chart"
    p.grid.grid_line_alpha = 0.3

    hours_12 = 12 * 60 * 60 * 1000

    p.segment(df.index, df.High, df.index, df.Low, color="Black")
    p.rect(df.index, df.Middle, hours_12, df.Height, fill_color=df.color, line_color='black')

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("plot.html",
                           script1=script1,
                           div1=div1,
                           cdn_css=cdn_css,
                           cdn_js=cdn_js)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

# NOTA: Este fuente está en la Raspberry Pi, en el directorio /home/pi/Website. Hará de servidor
# También se ha creado la carpeta templates y alojado el documento home.html y about.html
# Abrir con Thonny y pulsar play
# Ejecutar en el cliente desde el navegador escribiendo una de las dos
# 192.168.1.25:5000/
# 192.168.1.25:5000/about/

# Nota:
# Para crear un entorno virtual ir a la carpeta donde están los fuentes y escribir
# python3 -m venv virtual
# la m es de módules
# Esto instala Python en ese directorio, sin los módulos que tenemos ya instalados en el Python "principal"
# Así que para instalar vamos a nuestra nueva versión de Python e instalamos normalmente con pip3
# Hay que entrar en la carpeta bin y ahí escribir pip3 install flask