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
            'grayscale':{
                # link
                # ex:
                # [
                #    'href="bootsrap.css" type="text/css" rel="stylesheet"',
                #    'href="bootstrapthemes.css" type="text/css" rel="stylesheet"'
                # ]
                'link':[
                    'href="/contents/grayscale/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet"',
                    'href="/contents/grayscale/vendor/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css"',
                    'href="https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic" rel="stylesheet" type="text/css"',
                    'href="https://fonts.googleapis.com/css?family=Cabin:700" rel="stylesheet" type="text/css"',
                    'href="/contents/grayscale/css/grayscale.min.css" rel="stylesheet"'
                ],

                # script source
                # ex:
                # [
                #    'src="bootstrap.js" type="text/babel"',
                #    'src="bootstrapthemes.js" type="text/javascript"'
                # ]
                'script':[
                    'src="/contents/grayscale/vendor/jquery/jquery.min.js"',
                    'src="/contents/grayscale/vendor/bootstrap/js/bootstrap.bundle.min.js"',
                    'src="/contents/grayscale/vendor/jquery-easing/jquery.easing.min.js"',
                    'src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCRngKslUGJTlibkQ3FkfTxj3Xss1UlZDA&sensor=false"',
                    'src="/contents/grayscale/js/grayscale.min.js"'
                ],

                # meta source
                # ex:
                # [
                #    'charset="UTF-8"',
                #    'name="description" content="Free Web tutorials"',
                #    'name="keywords" content="HTML,CSS,XML,JavaScript"',
                #    'name="author" content="John Doe"',
                #    'name="viewport" content="width=device-width, initial-scale=1.0"',
                # ]
                'meta':[
                    'charset="utf-8"',
                    'name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"',
                    'name="description" content=""',
                    'name="author" content=""'
                ]
            },
            'others':{
                'link':[

                ],
                'script':[

                ],
                'meta':[

                ]
            }
        }

        return scripts
        