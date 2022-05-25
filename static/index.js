const paste = document.getElementById('paste');
const clearBtn = document.getElementById('clear');
const notesModal = document.getElementById("notesModal");
const infoBtn = document.getElementById("infoBtn");
const modalCloseBtn = document.getElementById("modalCloseBtn");
const submitBtn = document.getElementById("submitBtn");
const loader = document.getElementById("loader");
const MIMETYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document";

const isValidHttpUrl = string => {
    let url;
    
    try {
      url = new URL(string);
    } catch (_) {
      return false;  
    }
    if(url.protocol !== "http:" && url.protocol !== "https:"){
        return false;
    }
    return (url.host.toLowerCase() === "www.jw.org");
}

const randomIntFromInterval = (min=10000, max=99999) => {
    return Math.floor(Math.random() * (max - min + 1) + min)
}

paste.addEventListener('click', () => {
    navigator.clipboard.readText().then((clipText) => {
        console.log(clipText);
        document.getElementById('article-link').value = clipText;
    });
});

clearBtn.addEventListener('click', () => {
    document.getElementById('article-link').value = "";
    document.getElementById('article-title').value = "";
});



// When the user clicks on the button, open the modal
infoBtn.onclick = function() {
    notesModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
modalCloseBtn.onclick = function() {
    notesModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == notesModal) {
        notesModal.style.display = "none";
    }
}

submitBtn.onclick = function(_) {

    const link_obj = document.getElementById('article-link');
    const link_value = link_obj.value;
    if(!link_value) {
        alert( "Please provide a link!" );
        link_obj.focus();
        return;
    }

    if(!isValidHttpUrl(link_value)) {
        alert( "Please provide a valid JW.org link!" );
        link_obj.focus();
        return;
    }
    const json={
        article_link : link_value,
        article_title : document.getElementById('article-title').value
    };
    const options={
        method: "POST",
        body: JSON.stringify(json)
    };
    loader.classList.add("is-active");
    fetch('/',options)
    .then(response=>{
        loader.classList.remove("is-active");
        if (!response.ok) {
            throw Error(response.statusText); 
        }
        return response.blob();
    }).then(blob=>{
        download(blob, `article-doc-${randomIntFromInterval()}.docx`, MIMETYPE);
    }).catch(err=> {
        alert("Opps!! Something is wrong somewhere. Please try another link.");
    });
}