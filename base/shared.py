class Shared():

    # return shared data used by template
    def data(self):

        data = {
            'page_title':'FlyBee Grayscale - Start Bootstrap Theme',
            }

        return data


    # return client script used by template
    # css and script resource
    def clientScripts(self):

        scripts = {
            'reactjs_sample':{
                'link':[
                    #'href="/contents/grayscale/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet"',
                    #'href="/contents/grayscale/vendor/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css"',
                ],
                'script':[
                    'src="/templates/reactjs_sample/js/react/react.production.min.js"',
                    'src="/templates/reactjs_sample/js/react/react-dom.production.min.js"',
                    'src="/templates/reactjs_sample/js/react/babel.min.js"'
                ],
                'meta':[
                    #'charset="utf-8"',
                    #'name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"',
                ]
            }
        }

        return scripts
        