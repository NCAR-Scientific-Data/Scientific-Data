window.onload = function(){
    var select = document.getElementById("model");
    var folder = "/Users/Bobby/College Senior/Senior Projects/Scientific Data/tangelo_html/netCDF"
    for(var i = 0; i <= 10; i++) {
    	var myObject = new ActiveXObject("Scripting.FileSystemObject");
    	var f = myObject.GetFolder(folder);
      	filesCount = f.files.Count;
        option = document.createElement("option");
        option.value = filesCount;
        option.innerHTML = filesCount;
        select.appendChild(option);
    }
};
