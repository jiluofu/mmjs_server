package main


import (
    "fmt"
    "net/http"
    // "net/url"
    "os"
    "io/ioutil"
    "encoding/json"
    "strings"
    "log"
)

// const prefixPath string = "/Users/zhuxu/Documents/gohttps/static/imgs"
// const prefixUrl string = "https://127.0.0.1:8081/imgs"

// windows配置
const prefixPath string = "/home/zhuxu/gohttps/static/imgs"
const prefixUrl string = "http://home.momiaojushi.com:8081/imgs"
const prefixAudioPath string = "/home/zhuxu/gohttps/static/audios"
const prefixHomeUrl string = "http://home.momiaojushi.com:8081"

func handler(w http.ResponseWriter, r *http.Request) {

    log.Printf("%s,%s", r.RemoteAddr, r.URL)


    q := r.URL.Query()

    if q.Get("get_folders") == "1" {

       /* files, _ := listDir(prefixPath)
        // fmt.Println(files)

        res, _ := json.Marshal(files)
        fmt.Fprintf(w, "%s", string(res))
	res, _ := json.Marshal(files)*/
        resp, _ := http.Get(prefixHomeUrl + "/?get_folders=1")
	// fmt.Println(prefixHomeUrl + "/?get_folders=1")
        defer resp.Body.Close()
        body, _ := ioutil.ReadAll(resp.Body)
	//fmt.Println(string(body))
        fmt.Fprintf(w, "%s", string(body))

    } else if q.Get("get_files_by_folder") != "" {

        dir := q.Get("get_files_by_folder")
/*
        path := prefixPath + string(os.PathSeparator) + dir

        files, _ := listFiles(path, dir)
        // fmt.Println(files)

        res, _ := json.Marshal(files)*/
	resp, _ := http.Get(prefixHomeUrl + "/?get_files_by_folder=" + dir)
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
        fmt.Fprintf(w, "%s", string(body))
    } else if q.Get("get_audios") != "" {


        files, _ := listAudioFiles(prefixAudioPath)
        // fmt.Println(files)

        res, _ := json.Marshal(files)
        fmt.Fprintf(w, "%s", string(res))
    } else {
    	
    	fmt.Fprintf(w, "Welcome to MOMIAOYA. Any questions please contact to zhu.xu@qq.com.")
    	
    }



}

func listDir(dirPth string)  (files []string, err error) {

    files = make([]string, 0, 100)

    dir, _ := ioutil.ReadDir(dirPth)



    // PthSep := string(os.PathSeparator)


    for _, fi := range dir {

        if fi.IsDir() { // 忽略目录

            files = append(files, fi.Name())
        }
    }

    return files, err

}

func listFiles(dirPth string, dirName string)  (files []string, err error) {

    files = make([]string, 0, 100)

    dir, _ := ioutil.ReadDir(dirPth)


    for _, fi := range dir {

        if !fi.IsDir() { // 忽略目录

            if strings.HasSuffix(strings.ToLower(fi.Name()), ".jpg") {

                files = append(files, prefixUrl + "/" + dirName + "/output/" + fi.Name())
            }


        }
    }

    return files, err

}

func listAudioFiles(dirPth string)  (files []string, err error) {

    files = make([]string, 0, 1000)

    dir, _ := ioutil.ReadDir(dirPth)


    for _, fi := range dir {

        if !fi.IsDir() { // 忽略目录

            if strings.HasSuffix(strings.ToLower(fi.Name()), ".m4a") {

                files = append(files, fi.Name())
                files = append(files, fi.Name())
                files = append(files, fi.Name())
                files = append(files, fi.Name())
                files = append(files, fi.Name())
                files = append(files, fi.Name())
                files = append(files, fi.Name())
                files = append(files, fi.Name())
                files = append(files, fi.Name())
            }


        }
    }

    return files, err

}

var logfile *os.File
var logger *log.Logger

func main() {

    logfile, _ = os.Create("test.log")
    logger = log.New(logfile, "", log.LstdFlags|log.Llongfile)
    log.Println("start...")
    logger.Println("start...")

    http.Handle("/imgs/", http.FileServer(http.Dir("static")))
    http.Handle("/audios/", http.FileServer(http.Dir("static")))
    http.Handle("/weather/", http.FileServer(http.Dir("static")))
    http.Handle("/weather/output/", http.FileServer(http.Dir("static")))
    http.HandleFunc("/", handler)
 

    _, err := os.Open("cert_server/www.momiaojushi.com.2019.crt")
    if err != nil {
      panic(err)
    }

    log.Println("HTTPS Server started on 443")
    resp := http.ListenAndServeTLS(":443", "cert_server/www.momiaojushi.com.2019.crt", "cert_server/www.momiaojushi.com.2019.key", nil)
    fmt.Println(resp)

}


