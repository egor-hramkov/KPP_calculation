import axios from "axios";

export class kppApi {
    get() {
        return axios.get('http://localhost:8080')
    }
}