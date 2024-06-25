document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("callPythonFunction").addEventListener("click", function() {
        fetch("/call_python_function", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ data: "test" }) // Předání dat serveru
        })
        .then(response => response.json())
        .then(data => {
            alert("Response from Python: " + data.result);
        });
    });
});
