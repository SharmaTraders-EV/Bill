var counter=1

function addmoreP()
{
    counter+=1
    var html1='<div class="col-md-12">\
    <input class="form-control" type="text" name="pname" placeholder="Product Name" required>\
 </div>\
 <div class="col-md-12">\
     <input class="form-control" type="text" name="pcode" placeholder="Product Code" required>\
 </div>\
<div class="col-md-12">\
   <input class="form-control" type="text" name="pprice" placeholder="Product Price" required>\
</div>\
<hr>'

if (counter<100){
    var x=document.getElementById("pinfo")
    x.innerHTML+=html1
    var y = document.getElementById("counter")
    y.value=counter
    }
}