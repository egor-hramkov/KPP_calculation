import axios from "axios";

export class kppApi {
    get() {
        // const options_ = {
        //     method: "GET",
        //     headers: {
        //         "Accept": "application/json",
        //         "Access-Control-Allow-Origin": "*"
        //     }
        // };
        return axios.get('http://localhost:8080')
    }
}