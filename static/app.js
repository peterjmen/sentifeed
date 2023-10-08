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

