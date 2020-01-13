$(document).ready(function () {
    $('#newTodo').trigger('focus')
    $('#listSelector').on('change', switchList)
});

function switchList() {
    var url = $('#listSelector').val();
    if (url && url.length) {
        location.href = url;
    }
}

function formatDealer(value, row, index) {
    return "<a href='/dealer/" + value + "'>" + value + "</a>";
}

function formatVin(value, row, index) {
    return "<a href='/car/" + value + "'>" + value + "</a> - <a href='https://www.kia.com/us/services/en/windowsticker/load/" + value + "' target='_blank'>Sticker</a>";
}

function formatOptions(value, row, index) {
    switch (value) {
        case "027":
        case "025":
            return "P/T";
        case "022":
        case "020":
            return "P";
        case "017":
            return "T";
        case "015":
            var model = row.car_model;
            if (model === "J4482" || model === "J4282") {
                return "T";
            }
        default:
            return "";
    }
}

function formatModel(value, row, index) {
    var models =
        {
            'J4482': 'SX V6 AWD',
            'J4442': 'EX V6 AWD',
            'J4282': 'SX V6 FWD',
            'J4422': 'LX V6 AWD',
            'J4242': 'EX V6 FWD',
            'J4432': 'S V6 AWD',
            'J4222': 'LX V6 FWD',
            'J4232': 'S V6 FWD'
        };
    return models[value];
}
