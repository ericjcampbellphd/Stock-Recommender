from flask import Flask, render_template, request, url_for
from table import get_table 
from plot import get_plot

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/motivation')
def motivation():
    return render_template('motivation.html')

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/algorithm', methods=['GET', 'POST'])
def algorithm():
    if request.method == 'GET':
        return render_template('algorithm.html')
    else:
        form_results = {}
        year = request.form.get('year')
        quarter = request.form.get('quarter')
        form_results['year'] = year
        form_results['quarter'] = quarter

        table_data = get_table(int(year), int(quarter))
        form_results['table_data'] = table_data

        plot_data = get_plot(int(year), int(quarter))
        form_results['plot_data'] = plot_data

        #return render_template('plot.html')
        return render_template('algorithm_response.html',form_results=form_results)

if __name__=='__main__':
    app.run(debug=True)
