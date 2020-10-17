function fadeOut(element) {
    return new Promise((resolve, reject) => {
        try {
            let op = 1;
            let timer = setInterval(() => {
                if (op <= 0.1) {
                    clearInterval(timer);
                    element.style.display = 'none';
                    resolve();
                } else {
                    element.style.opacity = op;
                    element.style.filter = 'alpha(opacity=' + op * 100 + ")";
                    op -= op * 0.2;
                }
            }, 40);
        } catch (e) {
            reject()
        }
    })

}

function fadeIn(element) {
    return new Promise((resolve, reject) => {
        try {
            element.style.opacity = '0';
            element.style.display = 'block'
            let op = 0.1;  // initial opacity
            let timer = setInterval(() => {
                if (op > 0.95) {
                    clearInterval(timer);
                    element.style.opacity = 1;
                    resolve();
                } else {
                    element.style.opacity = op;
                    element.style.filter = 'alpha(opacity=' + op * 100 + ")";
                    op += op * 0.2;
                }
            }, 40);
        } catch (e) {
            reject()
        }
    })
}

const analyse = async () => {
    if (document.getElementById("tweet").textLength) {
        document.getElementById("anabutton").disabled = true;
        await fadeOut(document.getElementById("text_input"));
        await fadeIn(document.getElementById("responseholder"))
        fetch('https://ai.tibovanheule.space/api/analyse', {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({message: document.getElementById("tweet").value})
        }).then(data => data.text()).then(data => {
            console.log(data);
            document.getElementById("response").innerHTML = data;


            fadeIn(document.getElementById("validate"));
        });
    }
}


const validate = async (bool) => {document.getElementById("yes").disabled = true;
    document.getElementById("no").disabled = true;
    fetch('https://ai.tibovanheule.space/api/validate', {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({validate: bool, message: document.getElementById("tweet").value})
    }).then(data => data.text()).then(data => {
        console.log(data);
        document.getElementById("validatingtext").innerHTML = "Thank you for your response";
        fadeOut(document.getElementById("buttons"));
    });
}
