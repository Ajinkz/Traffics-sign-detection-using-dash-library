import skimage
from skimage import data,io
from PIL import Image
import io
import base64 
import numpy as np
from keras.models import load_model
import tensorflow as tf
# loading model
model = load_model('TSD.h5')
# Initial tf graph
global graph
graph = tf.get_default_graph()
# dictationary: key[id] mapped with its value[name] 
dict1 = {'[0]': 'single speed breaker','[1]': 'double bump breaker','[2]':'Slippery road','[3]':'Dangerous left curve ','[4]':'Dangerous right curve','[5]':'Left curve followed by right curve','[6]':'Right curve followed by left curve','[7]':'Place where a lot of children come','[8]':'Bicycle crossing ','[9]':'No Supported file','[10]':'Construction ','[12]':'Railway crossing with gates','[13]':'Caution sign under it details the danger','[14]':'Road narrows ','[16]':'Road narrows ','[17]':'Priority at next intersection','[18]':'Intersection with priority to the right','[19]':'Give way','[20]':'Two-way traffic after part with one-way traffic','[21]':'Stop and give way','[22]':'No entry (no application for pedestrians)','[23]':'No entry for bicycles','[24]':'No entry for vehicles with more mass than indicated','[25]':'No entry for vehicles used for goods transport Can be added with a sign indicating maximum mass.','[27]':'No entry for vehicles which are wider than indicated','[28]':'No entry in both directions (no application for pedestrians)','[29]':'No turn in the direction of the arrow allowed at intersection','[30]':'No turn in the direction of the arrow allowed at intersection','[31]':'No overtaking of vehicles with more than two wheels until the next intersection','[32]':'max speed 70 kmph','[34]':'Mandatory to follow the direction indicated by the arrow','[35]':'Mandatory to follow the left direction ','[37]':'Roundabout','[38]':'Mandatory cycleway (cyclists and mofas must use it)','[39]':'Part of the road reserved for pedestrians, cyclists and mofas (also mandatory to use it)','[40]':'No parking allowed An extra sign can indicate when the prohibition is in force','[41]':'No parking or standing still allowed An extra sign can indicate when the prohibition is in force','[42]':'No parking allowed on this side of the road from 1st day of the month until the 15th','[43]':'No parking allowed on this side of the road from the 16th day of the month until the last','[44]':'two way','[45]':'indicate parking','[46]':'parking only for disabled drivers','[47]':'Parking exclusively for motorcycles, motorcars and minibuses','[49]':'Parking exclusively for tourist buses','[51]':'Start of wooner zone résidentielle or zone de rencontre', '[53]':'Mandatory to follow the straight direction ','[55]':'End of road works','[56]':'Pedestrian crossing','[57]':'Bicycle and moped crossing','[58]':'Indicating parking','[59]':'Speed bump','[60]':'End of priority road','[61]':'Priority road'}
# Dash components
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
# CSS file
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.config.supress_callback_exceptions = True

# main layout
app.layout = html.Div([
    html.H1("Traffic Sign Detection"),
    dcc.Upload(id='upload-image',children=html.Div(['Drag and Drop or ',html.A('Select Files')]),
        style={
            'width': '50%',
            'height': '30%',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),
    # html.H3(id="sym_name"),
])


def parse_contents(contents, filename, date):
    """Parse image string(base64) format and disply using img tag"""
    # length=len(contents)
    sign=detect_sign(contents)
    return html.Div([
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents, style={"width":'30%',"height":"30%",'margin': '10px'}),
        html.H4(sign),
    ])


def find_img_type(strng):
    """find the image/file format"""
    format=(strng.split(",",1)[0]).split("/")[1][:-7]
    return format

def detect_sign(contents):
    """To convert image string into PIL form and perform detection operation"""
    strng=contents
    if find_img_type(strng)=='jpeg':
        type1=strng[23:]#jpeg
        str2img =Image.open(io.BytesIO(base64.b64decode(type1)))
        imx=np.array(str2img)
    #     print(imx.shape)
        img = skimage.transform.resize(imx, (32, 32), mode='constant')
        img1 = np.reshape(img,[1,32,32,3])
        with graph.as_default():
            classes = model.predict_classes(img1)

        for i in dict1.keys():
            if i == str(classes):
                name = dict1[i]
                print("Image :",name)
        return name

    elif find_img_type(strng)=='png':
        type2=strng[22:]#png
        str2img =Image.open(io.BytesIO(base64.b64decode(type2)))
        imx=np.array(str2img)
        print(imx.shape)
        Im4=imx[:,:,:-1]
        img = skimage.transform.resize(Im4, (32, 32), mode='constant')
        img1 = np.reshape(img,[1,32,32,3])
        with graph.as_default():
            classes = model.predict_classes(img1)

        for i in dict1.keys():
            if i == str(classes):
                name = dict1[i]
                print("Image :",name)
        return name

    elif find_img_type(strng)=='octet-stream':
        type3=strng[37:] #ppm
        str2img =Image.open(io.BytesIO(base64.b64decode(type3)))
        imx=np.array(str2img)
        print(imx.shape)
        img = skimage.transform.resize(imx, (32, 32), mode='constant')
        img1 = np.reshape(img,[1,32,32,3])
        with graph.as_default():
            classes = model.predict_classes(img1)

        for i in dict1.keys():
            if i == str(classes):
                name = dict1[i]
                print("Image :",name)
        return name

    else:
        msg="File format not supported.Please upload image with .jpeg/.png/.ppm format only"
        return msg

# To display uploaded image file
@app.callback(
              Output('output-image-upload', 'children'),
              # Output('sym_name', 'children')],
              [Input('upload-image', 'contents')],
              [State('upload-image', 'filename'),
               State('upload-image', 'last_modified')]
               )
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        visual = [ parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]                                                                
        # print(len(visual))
        return visual


if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port=8080)
 