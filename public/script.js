document.addEventListener('DOMContentLoaded', (event) => {
    fetch('/api/strategies')
        .then(response => response.json())
        .then(data => {
            let strategy1Select = document.getElementById('strategy1');
            let strategy2Select = document.getElementById('strategy2');

            data.forEach(strategy => {
                let option1 = document.createElement('option');
                option1.value = strategy;
                option1.text = strategy;
                strategy1Select.add(option1);

                let option2 = document.createElement('option');
                option2.value = strategy;
                option2.text = strategy;
                strategy2Select.add(option2);
            });
        });

    document.getElementById('gameForm').addEventListener('submit', function(e) {
        e.preventDefault();
        fetch('/api/play', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                strategy1: document.getElementById('strategy1').value,
                strategy2: document.getElementById('strategy2').value,
                rounds: parseInt(document.getElementById('rounds').value)
            }),
        })
        .then(response => response.json())
        .then(data => {
            let resultsHtml = '<h2>Results:</h2>';
            data.results.forEach(result => {
                resultsHtml += `<p>Round ${result.round}: Bot1 ${result.choice1}, Bot2 ${result.choice2} - Bot1: ${result.m1}, Bot2: ${result.m2}</p>`;
            });
            resultsHtml += `<h3>Final Score - Bot1: ${data.final_m1}, Bot2: ${data.final_m2}</h3>`;
            resultsHtml += `<h3>Result: ${data.winner}</h3>`;
            document.getElementById('results').innerHTML = resultsHtml;
        });
    });
});
