function formatDealer(value, row, index) {
    return "<a href='/dealer/" + value + "'>" + value + "</a>";
}

function formatVin(value, row, index) {
    return "<a href='https://ev-scraper.herokuapp.com/kia/windowsticker?vin=" + value + "' target='_blank' rel='noopener noreferrer'>" + value + "</a>";
}

function formatOptions(value, row, index) {
    switch (value) {
        case "027":
        case "025":
            return "P/T";
        case "022":
        case "020":
            return "PRE";
        case "017":
            return "TOW";
        case "035":
            var model2 = row.car_model;
            if (model2 == "J4442") {
                return "N/T/P";
            }
            else {
                return "T/N";
            }
	case "030":
            var model3 = row.car_model;
            if (model3 == "J4442") {
                return "P/N";
            }
            else {
                return "NE";
            }
	case "032":
		return "NE";
	case "037":
		return "T/N";
	case "040":
        case "042":
		return "P/N";
	case "045":
	case "047":
		return "N/T/P";
	        case "015":
            var model = row.car_model;
            if (["J4482", "J4282", "J4442", "J4242"].indexOf(model) >= 0) {
                return "TOW";
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

function formatDate(value, row, index){
    return moment(value).format('L');
}

function formatInteriorColor(value, row, index){
    switch (row.opt_code){
        case "012":
        case "017":
	case "032":
	case "037":
            return "BUTTERSCOTCH";
        case "022":
        case "027":
	case "042":
	case "047":
            return "DUNE BROWN";
        default:
            return value;

    }
    return value;
}
