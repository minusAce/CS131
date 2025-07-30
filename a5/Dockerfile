FROM apache/spark-py:latest

USER root
RUN pip install numpy pandas seaborn matplotlib

WORKDIR /app
COPY . .

# download dataset, execute Spark app and output to `output.txt`, generate plots, and clean dir.
CMD bash -c "\
curl -sSL https://archive.ics.uci.edu/ml/machine-learning-databases/car/car.data -o car.data && \
/opt/spark/bin/spark-submit sample.py > output.txt && \
mkdir -p predictions plots && \
mv out/cost_eval/part-00000*.csv predictions/cost.csv && \
mv out/util_eval/part-00000*.csv predictions/util.csv && \
python3 visualize.py && \
rm -rf out out_flat car.data __pycache__"
