#########################################################################
# Dicomifier.ws - Copyright (C) Universite de Strasbourg
# Distributed under the terms of the MIT license. Refer to the 
# LICENSE.txt file or to https://opensource.org/licenses/MIT for details.
#########################################################################

import werkzeug
import dicomifier_ws

werkzeug.run_simple(
    "127.0.0.1", 5000, dicomifier_ws.Application.instance(), 
    use_debugger=True, use_reloader=True)
