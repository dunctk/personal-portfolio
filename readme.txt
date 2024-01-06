To deploy:

workon ladderfunnel
cd ladderfunnel/ladderfunnel
python manage.py tailwind build
cd distill
python ../ladderfunnel/manage.py distill-local "/Users/dunc/Library/Mobile Documents/com~apple~CloudDocs/Active Code Projects/ladderfunnel/distill/output" --collectstatic
git add .
git commit -m "commit message"
git push