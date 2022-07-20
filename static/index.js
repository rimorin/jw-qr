const paste = document.getElementById('paste');
const clearBtn = document.getElementById('clear');
const notesModal = document.getElementById("notesModal");
const infoBtn = document.getElementById("infoBtn");
const modalCloseBtn = document.getElementById("modalCloseBtn");
const submitBtn = document.getElementById("submitBtn");
const loader = document.getElementById("loader");
const MIMETYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
const designSlides = document.querySelectorAll(".slide");
const maxSlide = designSlides.length - 1;
const nextSlideBtn = document.getElementById("nextBtn");
const prevSlideBtn = document.getElementById("prevBtn");
const mediaUrlKeys = ["mediaitems", "VIDEO"];
let currentSelectedSlide = 0;

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

const requiresTitle = (link, title) => {
  const isMediaKey = mediaUrlKeys.some(el => link.includes(el));
  if(isMediaKey && !title) return true;
  
  return false;
}

const randomIntFromInterval = (min=10000, max=99999) => {
    return Math.floor(Math.random() * (max - min + 1) + min)
}

const urlToHash = string => {
    let hash = 0;
    if (string.length == 0) return hash;
    for (let index = 0; index < string.length; index++) {
        char = string.charCodeAt(index);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return hash;
}

paste.addEventListener('click', () => {
    navigator.clipboard.readText().then((clipText) => {
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
    const title_obj = document.getElementById('article-title');
    const link_value = link_obj.value;
    const title_value = title_obj.value;
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

    if(requiresTitle(link_value, title_value)) {
        alert( "Please provide a title for media links!" );
        title_obj.focus();
        return;
    }
    const json={
        article_link : link_value,
        article_title : document.getElementById('article-title').value,
        article_design : currentSelectedSlide + 1
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
        download(blob, `QR${urlToHash(link_value)}.docx`, MIMETYPE);
    }).catch(err=> {
        alert("Opps!! Something is wrong somewhere. Please try another link.");
    });
}

// loop through slides and set each slides translateX
designSlides.forEach((slide, indx) => {
  slide.style.transform = `translateX(${indx * 100}%)`;
});

nextSlideBtn.onclick = function () {
  // check if current slide is the last and reset current slide
  if (currentSelectedSlide === maxSlide) {
    currentSelectedSlide = 0;
  } else {
    currentSelectedSlide++;
  }
  //   move slide by -100%
  designSlides.forEach((slide, indx) => {
    slide.style.transform = `translateX(${100 * (indx - currentSelectedSlide)}%)`;
  });
};

prevSlideBtn.onclick = function () {
  // check if current slide is the first and reset current slide to last
  if (currentSelectedSlide === 0) {
    currentSelectedSlide = maxSlide;
  } else {
    currentSelectedSlide--;
  }
  //   move slide by 100%
  designSlides.forEach((slide, indx) => {
    slide.style.transform = `translateX(${100 * (indx - currentSelectedSlide)}%)`;
  });
};