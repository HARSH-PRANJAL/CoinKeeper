const userName = document.querySelector("#usernameField");
const feedback = document.querySelector(".invalid-feedback1");
const userEmail = document.querySelector("#useremailField");
const emailfeedback = document.querySelector(".emailFeedBackArea");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const useremailSuccessOutput = document.querySelector(".useremailSuccessOutput");
const submitButton = document.querySelector(".submitButton");

userName.addEventListener("keyup", (e) => {
  const userNameVal = e.target.value;
  usernameSuccessOutput.style.display = "block";
  usernameSuccessOutput.textContent = `checking ${userNameVal}`;
  userName.classList.remove("is-invalid");
  feedback.style.display = "none";

  if (userNameVal.length > 0) {
    fetch("/authentication/validateUsername", {
      body: JSON.stringify({ username: userNameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        usernameSuccessOutput.style.display = "none";
        if (data.warning) {
          submitButton.disabled = true;
          userName.classList.add("is-invalid");
          feedback.style.display = "block";
          feedback.innerHTML = `<p>${data.warning}</p>`;
        } else {
          submitButton.removeAttribute("disabled");
        }
      });
  }
});

userEmail.addEventListener("keyup", (e) => {
  const userEmailVal = e.target.value;
  useremailSuccessOutput.style.display = "block";
  useremailSuccessOutput.textContent = `checking ${userEmailVal}`;
  userEmail.classList.remove("is-invalid");
  emailfeedback.style.display = "none";

  if (userEmailVal.length > 0) {
    fetch("/authentication/validateEmail", {
      body: JSON.stringify({ email: userEmailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        useremailSuccessOutput.style.display = "none";
        console.log("data", data);
        if (data.warning) {
          submitButton.disabled = true;
          userEmail.classList.add("is-invalid");
          emailfeedback.style.display = "block";
          emailfeedback.innerHTML = `<p>${data.warning}</p>`;
        } else {
          submitButton.removeAttribute("disabled");
        }
      });
  }
});
