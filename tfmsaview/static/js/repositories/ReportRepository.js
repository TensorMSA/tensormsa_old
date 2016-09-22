export default class ReportRepository {
    constructor(api) {
        this.api = api;
    }

    getConfigs(param) {
        return this.api.get(`/config/nn/${param}/param`).then((data) => {
            return data;
        });
    }

    postConfigs(params) {
        return this.api.post(`/config/nn/cnn/`, params).then((data) => {
            console.log(data);
           return data;
        });
    }

    postServices(params) {
        return this.api.post(`/service/nn/cnn/`, params).then((data) => {
           return data;
        });
    }
}