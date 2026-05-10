const form = document.querySelector("#idea-form");
const input = document.querySelector("#idea-input");
const resultTitle = document.querySelector("#result-title");
const resultList = document.querySelector("#result-list");

function buildResult(value) {
  const cleaned = value.trim() || "{{ONE_LINE_CONCEPT}}";
  return [
    `Core workflow: {{CORE_WORKFLOW}}`,
    `User input captured: ${cleaned.slice(0, 120)}`,
    "Next action: replace this demo transform with the project-specific behavior."
  ];
}

function render(items) {
  resultList.innerHTML = "";
  for (const item of items) {
    const li = document.createElement("li");
    li.textContent = item;
    resultList.appendChild(li);
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  resultTitle.textContent = "Generated result";
  render(buildResult(input.value));
});

render(buildResult(""));
