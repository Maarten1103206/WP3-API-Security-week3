let answeredCount = 0;
const totalStatements = 20;

$.get(`/api/student/${studentNumber}/info`, function (data) {
    $("#student-name").text(data.name);
    $("#student-class").text(data.class_name);
});

$(document).ready(function () {
    if (!studentNumber) {
        alert("Geen studentnummer gevonden.");
        window.location.href = "/";
        return;
    }

    function laadStelling() {
        $.get(`/api/student/${studentNumber}/statement`, function (data) {
            if (data.message === "Alle stellingen zijn al ingevuld.") {
                afronden();
            } else {
                $("#statement-number").text(data.statement_number);
                $("#choice1").text(data.statement_choices[0].choice_text);
                $("#choice2").text(data.statement_choices[1].choice_text);
                $("#choice1").data("choice", 1);
                $("#choice2").data("choice", 2);

                answeredCount++;
                const progress = Math.min((answeredCount / totalStatements) * 100, 100);
                $("#progress-bar").css("width", progress + "%");
                $("#progress-text").text(answeredCount);
            }
        });
    }

    function afronden() {
        $("#question-box").hide();
        $("#finished-box").show();

        // Optioneel: haal actiontype op (als je dat al bouwde)
        $.get(`/api/student/${studentNumber}/type`, function (data) {
            $("#action-type").text(data.action_type || "Onbekend");
        }).fail(function () {
            $("#action-type").text("Onbekend");
        });
    }

    $("button").click(function () {
        const choice = $(this).data("choice");
        const statementNumber = $("#statement-number").text();

        $.ajax({
            url: `/api/student/${studentNumber}/statement/${statementNumber}`,
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({statement_choice: choice}),
            success: function () {
                laadStelling();
            },
            error: function (err) {
                alert("Er ging iets mis: " + err.responseJSON?.error || err.statusText);
            }
        });
    });

    laadStelling();
});
