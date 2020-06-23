function sample_data(){
var sample_url = 'http://localhost:5001/point/sample';
fetch(sample_url).then(res => return res.json());
}
export {sample_data};