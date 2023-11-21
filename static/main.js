const random = (num) => {
    return Math.floor(Math.random() * num);
}
const getRandomStyles = () => {
    const top = random(100);
    const left = random(100);
    const dur = random(10) + 10;
    const size = random(25) + 25;
    return ` 
top: -${top}%; 
left: ${left}%; 
font-size: ${size}px; 
animation-duration: ${dur}s; 
`;
}
const createSnow = (num, isActive) => {
    if (window.isActiveVariable == undefined) window.isActiveVariable = isActive;
    const snowContent = ['&#10052', '&#10053']
    const snowContainer = document.getElementById("mainId");
    const button = document.getElementById("weihnachtsmodus");
    // document.body.style.background = "black";

    if (!window.isActiveVariable) {
        removeSnow();
        button.innerText = "In Weihnachtsmodus wechseln";
    }
    else {
        for (var i = num; i > 0; i--) {
            var snow = document.createElement("div");
            snow.className = "snow";
            snow.style.cssText = getRandomStyles();
            snow.innerHTML = snowContent[random(2)]
            snowContainer.append(snow);
        }
        button.innerText = "In Normalmodus wechseln";
        document.body.style.overflow = 'hidden';
        document.body.style.background = "#92b9f7";
    }
    window.isActiveVariable = !window.isActiveVariable;

}
const removeSnow = () => {
    var snowContainer = document.getElementsByClassName("snow");
    for (snowContainer.length; snowContainer.length > 0; snowContainer.length--) {
        snowContainer[0].remove();
    }
    document.body.style.background = "white";
}

function goBackFunction() {
    window.history.back();
}

function searchFunction() {
    var testEl = document.getElementById("test");
    testEl.style.display = "none";
}

function mapOnLoad() {
    console.log("test")
    var formClasses = document.getElementsByClassName("form-group");
    document.getElementById("submitButton").style.display = "none";
    for(var i = 0; i < formClasses.length; i++) {
        formClasses[i].style.display = "none";
    }
}