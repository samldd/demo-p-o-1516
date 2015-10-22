import mechanize, base64
br = mechanize.Browser()

br.open("https://netlogin.kuleuven.be")
br.select_form(name="wayf")
br.submit()
br.select_form(name="netlogin")
br["uid"] = "r0299448"
br[br.form.controls[3].name] = base64.b64decode("VGhyb3dhd2F5MTk5NHRv")
response = br.submit()
print response.read()