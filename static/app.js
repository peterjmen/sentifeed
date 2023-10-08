var isOpen = false;
function openNav() {
    if(isOpen === false){
        document.getElementById("filter").style.width = "250px";
        document.getElementById("articles").style.marginLeft = "250px";
        document.getElementById("mobile-header").style.marginLeft = "250px";
        isOpen = true
    }else {
        document.getElementById("filter").style.width = "0";
        document.getElementById("articles").style.marginLeft = "0";
        document.getElementById("mobile-header").style.marginLeft = "0";
        isOpen = false
    }    
}


var modal = document.getElementById("myModal");


var btn = document.getElementsByClassName("read-more-button");


var span = document.getElementsByClassName("close")[0];

var headline;
var content;
var url;


function setContent(head, con, link) {
    headline = head;
    content = con;
    url = link;
    console.log(head)
}


function showModal() {
    document.getElementById("modalHeadline").innerHTML = headline
    document.getElementById("modalContent").innerHTML = content
    document.getElementById("link").href = url
    modal.style.display = "block";
    
}

span.onclick = function() {
  modal.style.display = "none";
  
}
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}



