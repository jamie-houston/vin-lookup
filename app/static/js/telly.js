function formatDealer(value, row, index) {
    return "<a href='/dealer/" + value + "'>" + value + "</a>";
}

function formatVin(value, row, index) {
    return "<a href='https://ev-scraper.herokuapp.com/kia/windowsticker?vin=" + value + "' target='_blank' rel='noopener noreferrer'>" + value + "</a>";
}

function formatOptions(value, row, index) {
    var year = row.model_year;
    if (year == 2022) {
	switch (value) {
            case "027":
            case "025":
            case "045":
            case "047":
                return "P/T";
            case "022":
            case "020":
            case "040":
                return "PRE";
            case "017":
                return "TOW";
            case "035":
                var model2 = row.car_model;
                if (model2 == "J4442") {
                    return "P/T";
                }
                else {
                    return "TOW";
                }
            case "015":
                var model = row.car_model;
                if (["J4482", "J4282", "J4442", "J4242"].indexOf(model) >= 0) {
                    return "TOW";
                }
            case "030":
                var model3 = row.car_model;
                if (model3 == "J4442") {
                    return "P/N";
                }
                else {
                    return "BE";
                }
            case "037":
                return "T/N";
            case "040":
                return "P/N";
            case "042":
                return "N/T/P";
            default:
                return "";
        }
    }
    else {
        switch (value) {
            case "010": return "STD";
            case "012":
                var model = row.car_model;
                if (["J4242", "J4262", "J4462", "J4492"].indexOf(model) >= 0) {
                    return "MAH";
                }
                else if (["J4452", "J4472", "J4482", "J44A2", "J44B2"].indexOf(model) >= 0) {
                    return "TER";
                }
                else { return "" };
            case "014": return "SAG";
            case "015":
                var model = row.car_model;
                if (["J4262", "J4462", "J4492"].indexOf(model) >= 0) {
                    return "TOW";
                }
                else if (model == "J4242") {
                    return "CAP";
                }
                else if (model == "J4232") {
                    return "ROJ";
                }
            case "017":
                var model = row.car_model;
                if (["J4262", "J4462", "J4492"].indexOf(model) >= 0) {
                    return "TOW/MAH";
                }
                else if (model == "J4242") {
                    return "CAP/MAH";
                }
                else { return "" };
            case "020": return "CAP/TOW";
            case "022": return "CAP/TOW/MAH";
            default: return "";
        }
    }
}    

function formatModel(value, row, index) {
    var year = row.model_year;
    if (year == 2023) {
        switch (value) {
            case "J4222": return "LX V6 FWD";
            case "J4232": return "S V6 FWD";
            case "J4242": return "EX V6 FWD";
            case "J4262": return "SX V6 FWD";
            case "J4452": return "X-EX V6 AWD";
            case "J4462": return "SX V6 AWD";
            case "J4472": return "X-SX V6 AWD";
            case "J4482": return "XP-SX V6 AWD";
            case "J4492": return "SX-P V6 AWD";
            case "J44A2": return "X-SX-P V6 AWD";
            case "J44B2": return "XP-SX-P V6 AWD"
            };
    }
    else {
        switch (value) {
            case "J4482": return "SX V6 AWD";
            case "J4442": return "EX V6 AWD";
            case "J4282": return "SX V6 FWD";
            case "J4422": return "LX V6 AWD";
            case "J4242": return "EX V6 FWD";
            case "J4432": return "S V6 AWD";
            case "J4222": return "LX V6 FWD";
            case "J4232": return "S V6 FWD"
            };
}
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
