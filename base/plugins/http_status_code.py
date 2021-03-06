class HttpStatusCode():

    # informational response
    HTTP_CODE_CONTINUE = 100
    HTTP_CODE_SWITCHING_PROTOCOLS = 101
    HTTP_CODE_PROCESSING = 102
    HTTP_CODE_EARLY_HINTS = 103

    # success status code
    HTTP_CODE_OK = 200
    HTTP_CODE_CREATED = 201
    HTTP_CODE_ACCEPTED = 202
    HTTP_CODE_NON_AUTHORITATIVE_INFORMATION = 203
    HTTP_CODE_NO_CONTENT = 204
    HTTP_CODE_RESET_CONTENT = 205
    HTTP_CODE_PARTIAL_CONTENT = 206
    HTTP_CODE_MULTI_STATUS = 207
    HTTP_CODE_ALREADY_REPORTED = 208
    HTTP_CODE_IM_USED = 226

    # redirection status code
    HTTP_CODE_MULTIPLE_CHOICE = 300
    HTTP_CODE_MOVED_PERMANENTLY = 301
    HTTP_CODE_FOUND = 302
    HTTP_CODE_SEE_OTHER = 303
    HTTP_CODE_NOT_MODIFIED = 304
    HTTP_CODE_USE_PROXY = 305
    HTTP_CODE_SWITCH_PROXY = 306
    HTTP_CODE_TEMPORARY_REDIRECT = 307
    HTTP_CODE_PERMANENT_REDIRECT = 308

    # client error code
    HTTP_CODE_BAD_REQUEST = 400
    HTTP_CODE_UNAUTHORIZED = 401
    HTTP_CODE_PAYMENT_REQUIRED = 402
    HTTP_CODE_FORBIDDEN = 403
    HTTP_CODE_NOT_FOUND = 404
    HTTP_CODE_METHOD_NOT_ALLOWED = 405
    HTTP_CODE_NOT_ACCEPTED = 406
    HTTP_CODE_PROXY_AUTHENTICATION_REQUIRED = 407
    HTTP_CODE_REQUEST_TIMEOUT = 408
    HTTP_CODE_CONFLICT = 409
    HTTP_CODE_GONE = 410
    HTTP_CODE_LENGTH_REQUIRED = 411
    HTTP_CODE_PRECONDITION_FAILED = 412
    HTTP_CODE_PAYLOAD_TO_LARGE = 413
    HTTP_CODE_URI_TO_LONG = 414
    HTTP_CODE_UNSUPORTED_MEDIA_TYPE = 415
    HTTP_CODE_RANGE_NOT_SATISFIABLE = 416
    HTTP_EXPECTATION_FAILED = 417
    HTTP_CODE_IAM_TEAPOT = 418
    HTTP_CODE_MISDIRECT_REQUIRED = 421
    HTTP_CODE_UNPROCESSABLE_ENTITY = 422
    HTTP_CODE_LOCKED = 423
    HTTP_CODE_FAILED_DEPENDENCY = 424
    HTTP_CODE_UPGRADE_REQUIRED = 426
    HTTP_CODE_PRECONDITION_REQUIRED = 428
    HTTP_CODE_TO_MANY_REQUEST = 429
    HTTP_CODE_REQUEST_HEADER_FIELDS_TO_LARGE = 431
    HTTP_CODE_UNAVAILABLE_FOR_LEGAL_REASON = 451

    # server error
    HTTP_CODE_INTERNAL_SERVER_ERROR = 500
    HTTP_CODE_NOT_IMPLEMENTED = 501
    HTTP_CODE_BAD_GATEWAY = 502
    HTTP_CODE_SERVICE_UNAVAILABLE = 503
    HTTP_CODE_GATEWAY_TIMEOUT = 504
    HTTP_CODE_HTTP_VERSION_NOT_SUPPORTED = 505
    HTTP_CODE_VARIANT_ALSO_NEGOTIATES = 506
    HTTP_CODE_UNSUFFICIENT_STORAGE = 507
    HTTP_CODE_LOOP_DETECTION = 508
    HTTP_CODE_NOT_EXTENDED = 510
    HTTP_CODE_NETWORK_AUTHENTICATION_REQUIRED = 511

    # unofficial code
    HTTP_CODE_CHECKPOINT = 103
    HTTP_CODE_METHOD_FAILURE = 420
    HTTP_CODE_ENHANCE_YOUR_CALM = 420
    HTTP_CODE_BLOCKED_BY_WINDOWS_PARENTAL_CONTROL = 450
    HTTP_CODE_INVALID_TOKEN = 498
    HTTP_CODE_TOKEN_REQUIRED = 499
    HTTP_CODE_BANDWIDTH_LIMITED_EXCEEDDED = 509
    HTTP_CODE_SITE_FROZEN = 530
    HTTP_CODE_NETWORK_READ_TIMEOUT_ERROR = 598

    # internet information server
    HTTP_CODE_LOGIN_TIMEOUT = 440
    HTTP_CODE_RETRY_WITH = 449
    HTTP_CODE_REDIRECT = 451

    # nginx
    HTTP_CODE_NO_RESPONSE = 444
    HTTP_CODE_SSL_CERTIFICATE_ERROR = 495
    HTTP_CODE_SSL_CERTIFICATE_REQUIRED = 496
    HTTP_CODE_REQUEST_SEND_TO_HTTPS_PORT = 497
    HTTP_CODE_CLIENT_CLOSE_REQUEST = 499

    # cloudflare
    HTTP_CODE_UNKNOWN_ERROR = 520
    HTTP_CODE_WEBSERVER_IS_DOWN = 521
    HTTP_CODE_CONNECTION_TIMEOUT = 522
    HTTP_CODE_ORIGIN_IS_UNREACABLE = 523
    HTTP_CODE_TIMEOUT_OCCURED = 524
    HTTP_CODE_SSL_HANDSHAKE_FAILED = 525
    HTTP_CODE_INVALID_SSL_CERTIFICATE = 526
    HTTP_CODE_RAILGUNERROR = 527
