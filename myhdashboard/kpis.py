from read_data import read_data

df = read_data()

#selecting rows by .query() method
#alternative is: approved = df[df["Beslut"]== "Beviljad"]
#inside the expression, we don't need to use quotation/[] to refer to a column
#inside the expression, we can use single quotation to refer to string
approved = df.query("Beslut == 'Beviljad'")

#calculate kpis for all schools
number_approved = len(approved)
total_applications = len(df)
approved_precentage = f"{number_approved*100/total_applications:.1f}%"

#calculate kpis for one school
def provider_kpis(provider):
    applied = df.query(f"`Utbildningsanordnare administrativ enhet`== '{provider}'")
    applications = len(applied)
    approved = len(applied.query("Beslut=='Beviljad'"))

    return applications, approved


if __name__ == "__main__":
    #for testing purpose
    print(number_approved)
    print(total_applications)
    print(approved_precentage)
