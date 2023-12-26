import axios from "axios";

export class kppApi {
    get() {
        return axios.get('http://localhost:80')
    }
    post(data: any) {
        return axios.post('http://localhost:80', data)
    }
}