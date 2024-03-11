import streamlit as st
import pandas as pd

# Fonction pour charger les données à partir du fichier CSV
@st.cache_data
def get_Strats_data(file):
    df = pd.read_csv(file, delimiter=';')
    return df

# Page principale de l'application
def main():
    st.set_page_config(
        page_title="Application Horst de Dias",
        page_icon=":chart_with_upwards_trend:",  # Remplacez ceci par l'icône de votre choix
        layout="wide",  # Utilisez "centered" pour revenir à la largeur par défaut
        initial_sidebar_state="auto",
    )
    st.title("APP Horst de Dias")
    st.write("Bienvenue !")

    # Chargement automatique du fichier (utilisation d'un fichier par défaut)
    default_file_path = 'docs/Arnaud_BDD.csv'  # Remplacez ceci par le chemin de votre fichier par défaut
    uploaded_file = st.file_uploader("Chargez la base de données", type=["csv"], key="default_file", accept_multiple_files=False) or default_file_path

    # Widget de chargement de fichier
    # uploaded_file = st.file_uploader("Chargez la base de données", type=["csv"])

    # Vérifier si un fichier a été chargé
    if uploaded_file is not None:
        # Charger les données à partir du fichier
        df = get_Strats_data(uploaded_file)

        # Code pour ajouter une image arrondie en haut de la barre latérale
        # st.markdown(
        #     """
        #     <style>
        #         div:nth-child(1) > div.withScreencast > div > div > div > 
        #         section.st-emotion-cache-vk3wp9.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > 
        #         div.st-emotion-cache-16txtl3.eczjsme4 > div > div > div > div > div:nth-child(1) > div > div > div > 
        #         img {
        #             border-radius: 50%;
        #         }
        #     </style>
        #     """,
        #     unsafe_allow_html=True
        # )

        # Chemin local vers l'image dans le dossier "img"
        # rounded_image_path = "img/image1.png"  # Remplacez par le nom de votre image et son extension

        # Afficher l'image arrondie dans la barre latérale
        # st.sidebar.image(rounded_image_path, caption="", use_column_width=True, output_format="auto",)
        # Afficher les filtres dans la barre latérale
        st.sidebar.title("Recherche")

        # Créer un filtre interactif pour chaque colonne
        for column in df.columns:
            selected_values = st.sidebar.multiselect(f"Sélectionnez les valeurs pour {column}", df[column].unique())
            
            # Appliquer le filtre
            if selected_values:
                df = df[df[column].isin(selected_values)]

        # Remplacer -9,999 par NaN
        df.replace(to_replace=[-9.999, '-9.999', -9999, '-9999', '-9999.0'], value=pd.NA, inplace=True)

        # Afficher les données
        st.write("Logs stratigraphiques Horst de Dias")
        st.write(df)

        # Renommer les colonnes pour mieux faciliter le traitement et la cohérence
        # Liste des colonnes à renommer
        column_mapping = {
            'ZQ': 'Z_Quaternaire',
            'ZEO': 'Z_Éocène',
            'Zpa': 'Z_Paléocène',
            'Zmaa': 'Z_Maastrichtien',
            'Zca': 'Z_Campanien',
            'NPMaa': 'NP_Maastrichtien',
            'Tmaa': 'T_Maastrichtien',
            'NSPa': 'NS_Paléocène',
            'NPPa': 'NP_Paléocène',
            'Tpa': 'T_Paléocène',
            'Ppa': 'P_Paléocène',
            'LIAPa': 'LIA_Paléocène',
            'LSAPa': 'LSA_Paléocène',
            'EpaiPa': 'Epaisseur_Paléocène',
            'NSMaa': 'NS_Maastrichtien',
            'Pmaa': 'P_Maastrichtien',
            'EpaissQ': 'Epaisseur_Quaternaire',
            'EpaissMaa': 'Epaisseur_Maastrichtien',
            'LSAMaa': 'LSA_Maastrichtien',
            'LIAMaa': 'LIA_Maastrichtien',
            'EpaisEoc': 'Epaisseur_Éocène'
        }

        df_renamed = df.rename(columns=column_mapping)

        # Vérifier s'il y a des valeurs pour X et Y
        if 'X' in df_renamed.columns and 'Y' in df_renamed.columns and not df_renamed[['X', 'Y']].dropna().empty:
            # Afficher un avertissement si la requête dépasse 3 lignes
            if len(df_renamed) > 1:
                st.warning("La requête a retourné plus de 1 ligne. Veuillez préciser davantage les filtres pour réduire les résultats.")
            else:
                # Ajouter une ligne
                st.markdown("---")
                # Afficher les panneaux horizontaux pour chaque couche stratigraphique
                st.title("Panneaux Stratigraphiques")

                # Couche Quaternaire
                with st.container(border=True):
                    st.subheader("Informations sur la couche Quaternaire")
                    col11, col12, col13, col14, col15 = st.columns(5)
                    col21, col22, col23, col24, col25 = st.columns(5)

                    with col11:
                        st.write(f"<small>Z =  {str(df_renamed['Z_Quaternaire'].dropna().unique()[0]).replace('.',',')} m</small>" if not df_renamed["Z_Quaternaire"].dropna().empty else "<small>Aucune valeur</small>", unsafe_allow_html=True)
                        # Ajouter une ligne
                        # st.markdown("---")
                    with col12:
                        st.write(f"<small>Épaisseur = {str(df_renamed['Epaisseur_Quaternaire'].dropna().unique()[0]).replace('.',',')} m</small>" if not df_renamed["Epaisseur_Quaternaire"].dropna().empty else "<small>Aucune valeur</small>", unsafe_allow_html=True)
                        # Ajouter une ligne
                        # st.markdown("---")

                # Couche Éocène
                with st.container(border=True):
                    st.subheader("Informations sur la couche Éocène")
                    col11, col12, col13, col14, col15 = st.columns(5)
                    col21, col22, col23, col24, col25 = st.columns(5)

                    with col11:
                        display_metric_value(my_metric="Z",my_value=df_renamed['Z_Éocène'].dropna())
                    with col12:
                        display_metric_value(my_metric="Épaisseur",my_value=df_renamed['Epaisseur_Éocène'].dropna())

                # Couche Paléocène
                with st.container(border=True):
                    st.subheader("Informations sur la couche Paléocène")
                    col11, col12, col13, col14, col15 = st.columns(5)
                    col21, col22, col23, col24, col25 = st.columns(5)

                    with col11:
                        display_metric_value(my_metric="Z",my_value=df_renamed['Z_Paléocène'].dropna())
                    with col12:
                        display_metric_value(my_metric="NS",my_value=df_renamed['NS_Paléocène'].dropna())
                    with col13:
                        display_metric_value(my_metric="NP",my_value=df_renamed['NP_Paléocène'].dropna())
                    with col14:
                        display_scientific_value(my_metric="T",my_value=df_renamed['T_Paléocène'].dropna(), square=2)
                    with col15:
                        display_scientific_value(my_metric="P",my_value=df_renamed['P_Paléocène'].dropna())
                    with col21:
                        display_metric_value(my_metric="Épaisseur", my_value=df_renamed['Epaisseur_Paléocène'].dropna())
                    with col22:
                        display_metric_value(my_metric="LSA", my_value=df_renamed['LSA_Paléocène'].dropna())
                    with col23:
                        display_metric_value(my_metric="LIA", my_value=df_renamed['LIA_Paléocène'].dropna())

                # Couche Maastrichtien
                with st.container(border=True):
                    st.subheader("Informations sur la couche Maastrichtien")
                    col11, col12, col13, col14, col15 = st.columns(5)
                    col21, col22, col23, col24, col25 = st.columns(5)

                    with col11:
                        display_metric_value(my_metric="Z",my_value=df_renamed['Z_Maastrichtien'].dropna())
                    with col12:
                        display_metric_value(my_metric="NS",my_value=df_renamed['NS_Maastrichtien'].dropna())
                    with col13:
                        display_metric_value(my_metric="NP",my_value=df_renamed['NP_Maastrichtien'].dropna())
                    with col14:
                        display_scientific_value(my_metric="T",my_value=df_renamed['T_Maastrichtien'].dropna(), square=2)
                    with col15:
                        display_scientific_value(my_metric="P",my_value=df_renamed['P_Maastrichtien'].dropna())
                    with col21:
                        display_metric_value(my_metric="Épaisseur", my_value=df_renamed['Epaisseur_Maastrichtien'].dropna())
                    with col22:
                        display_metric_value(my_metric="LSA", my_value=df_renamed['LSA_Maastrichtien'].dropna())
                    with col23:
                        display_metric_value(my_metric="LIA", my_value=df_renamed['LIA_Maastrichtien'].dropna())


                # Couche Maastrichtien
                with st.container(border=True):
                    st.subheader("Informations sur la couche Campanien")
                    col11, col12, col13, col14, col15 = st.columns(5)
                    col21, col22, col23, col24, col25 = st.columns(5)

                    with col11:
                        display_metric_value(my_metric="Z",my_value=df_renamed['Z_Campanien'].dropna())

def display_scientific_value(my_metric, my_value, square=""):
    if not my_value.empty:
        # Séparation de la valeur et de l'exposant
        my_value = my_value.unique()[0]
        value_part, exponent_part = f"{my_value:.2e}".split("e")
        # Remplacer la point par une virgule (notation française)
        value_part = str(value_part).replace('.',',')
        return st.markdown(
            body=f"""
            <div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn3">
                <div data-testid="stVerticalBlockBorderWrapper" data-test-scroll-behavior="normal" class="st-emotion-cache-0 e1f1d6gn0">
                    <div class="st-emotion-cache-1wmy9hl e1f1d6gn1">
                        <div width="111.59375" data-testid="stVerticalBlock" class="st-emotion-cache-1m00g76 e1f1d6gn2">
                            <div data-stale="false" width="111.59375" class="element-container st-emotion-cache-gp88j e1f1d6gn4" data-testid="element-container">
                                <div class="stMarkdown" data-testid="stMarkdown" style="width: 150px;">
                                    <div data-testid="stMarkdownContainer" class="st-emotion-cache-eqffof e1nzilvr5">
                                        <p><small>{my_metric} =  {value_part}.10<sup>{int(exponent_part)}</sup> m<sup>{square}</sup>/s</small></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True)
    else:
        display_metric_value(my_metric,my_value)

def display_metric_value(my_metric, my_value):
    if not my_value.empty :
        # Séparation de la valeur et de l'exposant
        value = my_value.unique()[0]
        # Remplacer la point par une virgule (notation française)
        value = str(value).replace('.',',')
        return st.markdown(
            body=f"""
            <div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn3">
                <div data-testid="stVerticalBlockBorderWrapper" data-test-scroll-behavior="normal" class="st-emotion-cache-0 e1f1d6gn0">
                    <div class="st-emotion-cache-1wmy9hl e1f1d6gn1">
                        <div width="111.59375" data-testid="stVerticalBlock" class="st-emotion-cache-1m00g76 e1f1d6gn2">
                            <div data-stale="false" width="111.59375" class="element-container st-emotion-cache-gp88j e1f1d6gn4" data-testid="element-container">
                                <div class="stMarkdown" data-testid="stMarkdown" style="width: 150px;">
                                    <div data-testid="stMarkdownContainer" class="st-emotion-cache-eqffof e1nzilvr5">
                                        <p><small>{my_metric} = {value} m</small></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>            
            """,
            unsafe_allow_html=True)
    
    return st.markdown(
        body=f"""
        <div data-testid="column" class="st-emotion-cache-j5r0tf e1f1d6gn3">
            <div data-testid="stVerticalBlockBorderWrapper" data-test-scroll-behavior="normal" class="st-emotion-cache-0 e1f1d6gn0">
                <div class="st-emotion-cache-1wmy9hl e1f1d6gn1">
                    <div width="111.59375" data-testid="stVerticalBlock" class="st-emotion-cache-1m00g76 e1f1d6gn2">
                        <div data-stale="false" width="111.59375" class="element-container st-emotion-cache-gp88j e1f1d6gn4" data-testid="element-container">
                            <div class="stMarkdown" data-testid="stMarkdown" style="width: 150px;">
                                <div data-testid="stMarkdownContainer" class="st-emotion-cache-eqffof e1nzilvr5">
                                    <p><small>{my_metric} = Aucune valeur</small></p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True)
    



                

if __name__ == "__main__":
    main()
