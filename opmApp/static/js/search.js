$(document).ready(function() {
    $('#search-input').on('keyup', function() {
        let query = $(this).val();
        if (query.length > 0) {
            $.ajax({
                url: '{% url "search_patients" %}',
                data: { 'query': query },
                dataType: 'json',
                success: function(data) {
                    let resultsContainer = $('#suggestions');
                    resultsContainer.empty();
                    if (data.length > 0) {
                        data.forEach(function(item) {
                            let patientUrl = '{% url "patients_details" 0 %}'.replace('0', item.id);
                            resultsContainer.append(`
                                <div class="result-item">
                                    <a class="search_url" href="${patientUrl}">
                                        ${item.name} (${item.patient_id}) - ${item.email}
                                    </a>
                                    <hr>
                                </div>
                            `);
                        });
                    } else {
                        resultsContainer.append('<div class="result-item">No results found</div>');
                    }
                }
            });
        } else {
            $('#suggestions').empty();
        }
    });
});
 