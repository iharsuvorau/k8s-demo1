image = ARGV[0]

def build_publisher()
  puts "Building publisher"
  puts `docker build -t nokal/k8s-samples-wq-publisher:v2 -f publisher.dockerfile .`

  puts "Pushing publisher"
  puts `docker push nokal/k8s-samples-wq-publisher:v2`

  puts "Loading images into kind"
  puts `kind load docker-image nokal/k8s-samples-wq-publisher:v2`
end

def build_worker()
  puts "Building worker"
  puts `docker build -t nokal/k8s-samples-wq-worker:v2 -f worker.dockerfile .`

  puts "Pushing worker"
  puts `docker push nokal/k8s-samples-wq-worker:v2`

  puts "Loading images into kind"
  puts `kind load docker-image nokal/k8s-samples-wq-worker:v2`
end

if ["publisher", "pub", "p"].include?(image)
  build_publisher()
elsif ["worker", "work", "w"].include?(image)
  build_worker()
else
  build_publisher()
  build_worker()
end
