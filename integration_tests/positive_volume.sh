for i in 1..100
    do
        curl -s -o /dev/null -w '%{http_code}'  -X POST -F 'image=@images_samples/big.jpg' http://127.0.0.1:4555/upload &
    done
