/*
 Create temp form, and then fill up with require data
 and then submit it by post!
*/

function post(url, params)
{
    // post data by self post function
    // @param url: destination url
    // @param params: a dict-type
    
    var temp = document.createElement("form");
    temp.action = url;
    temp.method = "post";
    temp.style.display = "none";
    for (var x in params){
        var opt = document.createElement("textarea");
        opt.name = x;
        opt.value = params[x];
        temp.appendChild(opt);
        }
   document.body.appendChild(temp);
   temp.submit();
   return temp;
}


/*
 Post data by AJAX
*/

var createAjax = function () {
    var xhr = null;
    try {
        xhr = new ActiveXObject("microsoft.xmlhttp");
    } catch (e1) {
        try {
            xhr = new XMLHttpRequest();
        } catch (e2) {
            window.alert("您的浏览器不支持ajax，请更换！");
        }
    }
    return xhr;
};
var ajax = function (conf) {
    var type = conf.type;
    var url = conf.url;
    var data = conf.data;
    var dataType = conf.dataType;
    var success = conf.success;
    if (type == null) {
        type = "get";
    }
    if (dataType == null) {
        dataType = "text";
    }
    var xhr = createAjax();
    xhr.open(type, url, true);
    if (type == "GET" || type == "get") {
        xhr.send(null);
    } else if (type == "POST" || type == "post") {
        xhr.setRequestHeader("content-type",
            "application/x-www-form-urlencoded");
        xhr.send(data);
    }
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            if (dataType == "text" || dataType == "TEXT") {
                if (success != null) {
                    success(xhr.responseText);
                }
            } else if (dataType == "xml" || dataType == "XML") {
                if (success != null) {
                    success(xhr.responseXML);
                }
            } else if (dataType == "json" || dataType == "JSON") {
                if (success != null) {
                    success(eval("(" + xhr.responseText + ")"));
                }
            }
        } else if (xhr.readyState == 4 && xhr.status != 200) {
            //alert("请求失败!");
        }
    };
};

/* ---

*/
