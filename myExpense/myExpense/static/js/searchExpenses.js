const searchField = document.querySelector("#searchField");
const searchOutput = document.querySelector(".table2");
const oldTable = document.querySelector(".table1");
const pageNumbers = document.querySelector(".pageNumbers");
const tbody = document.querySelector(".table2-body");

searchOutput.style.display = "none";

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    tbody.innerHTML = "";
    pageNumbers.style.display = "none";
    console.log("searchValue", searchValue);
    fetch("/searchExpense", {
      body: JSON.stringify({ search: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        searchOutput.style.display = "block";
        oldTable.style.display = "none";
        if (data.length === 0) tbody.innerHTML = "No result found";
        else {
          data.forEach((element, index) => {
            tbody.innerHTML += `
              <tr>
                <td>${index + 1}</td>
                <td>${element.amount}</td>
                <td>${element.category}</td>
                <td>${element.description}</td>
                <td>${element.date}</td>
                <td>
                  <div class="container">
                    <div class="row">
                      <div class="col-md-3">
                        <form action="/updateExpense" method="GET">
                          <button class="btn btn-outline-success btn-sm" name="update" value="${
                            element.id
                          }"
                            data-bs-toggle="button" aria-pressed="true">
                            Edit
                          </button>
                        </form>
                      </div>
                      <div class="col-md-3">
                        <form action="/deleteExpense" method="POST">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                          <button class="btn btn-outline-danger btn-sm" name="delete" value="${
                            element.id
                          }"
                            data-bs-toggle="button" aria-pressed="true">
                            X
                          </button>
                        </form>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            `;
          });
        }
      });
  } else {
    searchOutput.style.display = "none";
    oldTable.style.display = "block";
    pageNumbers.style.display = "block";
  }
});
