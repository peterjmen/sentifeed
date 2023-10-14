// var to hold open state
var isOpen = false;
// function for handling menu open/close
function openNav() {
    
    if(isOpen === false){
        document.getElementById("filter").style.width = "80%";
        document.getElementById("mobile-header").style.marginLeft = "80%";
        isOpen = true
    }else {
        document.getElementById("filter").style.width = "0";
        document.getElementById("mobile-header").style.marginLeft = "0";
        isOpen = false
    }    
}

var modal = document.getElementById("myModal");
var btn = document.getElementsByClassName("read-more-button");
var span = document.getElementsByClassName("close")[0];

// variables for storing selected article content
var headline;
var content;
var url;

// funtion for setting content in modal
function setContent(head, con, link) {
    headline = head;
    content = con;
    url = link;
    console.log(head)
}

// function for showing model
function showModal() {
    document.getElementById("modalHeadline").innerHTML = headline
    document.getElementById("modalContent").innerHTML = content
    document.getElementById("link").href = url
    modal.style.display = "block";
    
}
// close modal
span.onclick = function() {
  modal.style.display = "none";
  
}
// close modal when clicking anywhere outside of modal
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}



