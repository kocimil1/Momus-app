from flask import Flask, render_template, jsonify

app = Flask(__name__)

from app import routes