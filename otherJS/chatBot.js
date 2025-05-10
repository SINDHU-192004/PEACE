var count = 0;

// THE BUTTONS ++++++++++++++++++++++++++++++++++++++++++++++

const startConvoBtn = document.querySelector('.start-convo-btn');
const speakBtn = document.querySelector('.speak-btn');
const stoConvoBtn = document.querySelector('.stop-convo-btn');
const talkBtn = document.querySelector('.talk-btn');

const startConvoBtnCont = document.querySelector('.start-convo-btn-cont');
const otherBtnCont = document.querySelector('.other-btn-cont');

const userSpeech = document.querySelector('.user-speech');

// Add information about the emotion detection
const botImgCont = document.querySelector('.bot-img-cont');
const emotionDetectionInfo = document.createElement('div');

botImgCont.appendChild(emotionDetectionInfo);

stoConvoBtn.addEventListener('click', () => {
    startConvoBtnCont.style.display = "block";

    speakBtn.style.display = "none";
    stoConvoBtn.style.display = "none";

    userSpeech.innerHTML = " ";

})


speakBtn.addEventListener('click', listenUser);


// ++++++++++++++++++++++++++++++++ P5 JS SETUP FOR SPEECH REGOGNITION

var speech = new p5.Speech();

var listenSpeech = new p5.SpeechRec('en-US');

function setup() {
    noCanvas();
    startSpeaking();
}

function welcome() {
    speech.speak(`Hello my friend im happy you're here. I can now detect your emotions to better understand how you're feeling.`);
}

function startSpeaking() {
    startConvoBtn.addEventListener('click', () => {
        count++;
        startConvoBtnCont.style.display = "none";

        speakBtn.style.display = "block";
        stoConvoBtn.style.display = "block";

        if (count === 1) {
            welcome();
        }
    })
}

// //////////////////////// RIVE SCRIPT SETUP ////////////////

var bot = new RiveScript();

bot.loadFile("../RiveScripts/botBrain.rive").then(loading_done).catch(loading_error);

function loading_done() {
    console.log("Bot has finished loading!");
    bot.sortReplies();
}

function loading_error() {
    console.log("Error!");
}

function listenUser() {
    listenSpeech.start(false, true);
    listenSpeech.onResult = startListen;

    listenSpeech.onStart = start;
    listenSpeech.onEnd = end;

    function startListen() {
        userSpeech.innerHTML = listenSpeech.resultString;
    }
}

function botReplay(message) {
    let username = "local-user";

    // Detect emotion using our Python API (note: this is simulated as the actual API call would require backend integration)
    let detectedEmotion = simulateEmotionDetection(message);
    
    // Display the detected emotion
    const emotionDisplay = document.createElement('div');
    emotionDisplay.innerHTML = `<p style="color: #6b7280; font-style: italic; margin-top: 5px;">Detected emotion: ${detectedEmotion}</p>`;
    userSpeech.appendChild(emotionDisplay);

    bot.reply(username, message).then(function (reply) {
        if (reply === "game section") {
            window.location.href = "../otherJS/carGame/games.html";
            return;
        }

        if (reply === "exercise section") {
            window.location.href = "../otherHTML/exercise.html";
            return;
        }

        if (reply === "food section") {
            window.location.href = "../otherHTML/food.html";
            return;
        }

        if (reply === "statistics section") {
            window.location.href = "../otherHTML/statistics.html";
            return;
        }

        // Add emotion context to the response
        let emotionContext = getEmotionContext(detectedEmotion);
        if (emotionContext) {
            reply = emotionContext + " " + reply;
        }

        speech.speak(reply);
    });
}

// This function simulates emotion detection (in a real implementation, this would call our Python API)
function simulateEmotionDetection(message) {
    // Simple keyword-based emotion detection as a fallback
    message = message.toLowerCase();
    
    if (message.includes("happy") || message.includes("joy") || message.includes("glad")) {
        return "joy";
    } else if (message.includes("sad") || message.includes("unhappy") || message.includes("depressed")) {
        return "sadness";
    } else if (message.includes("angry") || message.includes("mad") || message.includes("furious")) {
        return "anger";
    } else if (message.includes("scared") || message.includes("afraid") || message.includes("fear")) {
        return "fear";
    } else if (message.includes("love") || message.includes("adore")) {
        return "love";
    } else if (message.includes("thank") || message.includes("grateful")) {
        return "gratitude";
    } else if (message.includes("confused") || message.includes("unclear")) {
        return "confusion";
    } else if (message.includes("excited") || message.includes("thrilled")) {
        return "excitement";
    } else {
        return "neutral";
    }
}

// Get appropriate response based on detected emotion
function getEmotionContext(emotion) {
    const emotionResponses = {
        "sadness": "I can sense you're feeling down. ",
        "anger": "I understand you might be feeling frustrated. ",
        "fear": "It's okay to feel scared sometimes. ",
        "joy": "I'm glad you're feeling good! ",
        "love": "That's wonderful to hear. ",
        "gratitude": "It's nice to feel appreciated. ",
        "confusion": "Let me try to clarify things for you. ",
        "excitement": "I can feel your enthusiasm! "
    };
    
    return emotionResponses[emotion] || "";
}

// +++++++++++ Listening text ++++++

const listenText = document.querySelector('.listening-text');

function start() {
    listenText.classList.add("show-text");
    userSpeech.innerHTML = " ";
}

function end() {
    listenText.classList.remove("show-text");

    ///////// FEEDING INPUT TO BOT //////////

    if (listenSpeech.resultValue) {
        let userInteraction = listenSpeech.resultString;
        botReplay(userInteraction);
    }
}