let isOpen = false;

function openNav() {
    const filter = document.getElementById("filter");
    const articles = document.getElementById("articles");
    const mobileHeader = document.getElementById("mobile-header");
    
    if (isOpen) {
        filter.style.width = "0";
        articles.style.marginLeft = "0";
        mobileHeader.style.marginLeft = "0";
    } else {
        filter.style.width = "250px";
        articles.style.marginLeft = "250px";
        mobileHeader.style.marginLeft = "250px";
    }

    isOpen = !isOpen;
}

function setContent(headline, content, url) {
    const modalHeadline = document.getElementById('modalHeadline');
    const modalContent = document.getElementById('modalContent');
    const link = document.getElementById('link');
    const articleTitleHidden = document.getElementById('article-title-hidden');
    
    modalHeadline.textContent = headline;
    modalContent.textContent = content;
    link.href = url;
    articleTitleHidden.value = headline;
    
    showModal();
}

function showModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'block';
}

document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById('myModal');
    const closeSpan = document.querySelector('.close');
    
    closeSpan.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});
