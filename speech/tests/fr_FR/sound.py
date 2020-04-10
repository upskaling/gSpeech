import os
from os.path import join, dirname
import shutil
import tempfile
from hashlib import md5
from unittest import TestCase

from speech.textutils import adaptTextToDict
from speech.audioutils import getAudioCommands

assets_path = join(dirname(__file__), 'assets')
temp_path = tempfile.mkdtemp()

def create_sound(text, file_name):
    output_file = join(temp_path, '%s.wav' % file_name)
    lang = 'fr-FR'
    text = adaptTextToDict(
        text,
        join(dirname(dirname(dirname(dirname(__file__)))), 'dict', '%s.dic' % lang),
        lang
    )
    names, cmds = getAudioCommands(
        text,
        output_file,
        lang,
        join(os.getenv('HOME'), '.cache', 'gSpeech')
    )
    os.system(cmds[0])

def md5_sum(path, file_name):
    with open(join(path, '%s.wav' % file_name), 'rb') as f:
        return md5(f.read()).hexdigest()

def tmp_sum(file_name):
    return md5_sum(temp_path, file_name)

def asset_sum(file_name):
    return md5_sum(assets_path, file_name)


sounds = [
    [ 'Il aime son chat.', 'aime_son_chat' ],
    #[ 'Sam est un élève très doué', 'sam_eleve_doue' ],
    [ 'N\'oublie pas ton manteau', 'noublie_pas_ton_manteau' ],
    [ 'Tu veux du sucre dans ton yaourt ?', 'tu_veux_du_sucre_dans_ton_yaourt' ],
    [ 'Veux-tu manger une poire bien juteuse ?', 'veux_tu_manger_une_poire_bien_juteuse' ],
    [ 'Jeudi nous avons sport toute l\'après-midi.', 'jeudi_nous_avons_sport_toute_lapresmidi' ],
    [ 'J\'ai regardé un bon film hier soir.', 'jai_regarde_un_bon_film_hier_soir' ],
    [ 'Claire a une chevelure rousse.', 'claire_a_une_chevelure_rousse' ],
    [ 'Cette tache est invisible à l\'oeil nu.', 'cette_tache_est_invisible_a_loeil_nu' ],
    [ 'Je ne veux plus rien.', 'je_ne_veux_plus_rien' ],
    [ 'Ma bille a roulé sous l\'armoire.', 'ma_bille_a_roule_sous_larmoire' ],
    [ 'Passe-toi de l\'eau sur le visage.', 'passe_toi_de_leau_sur_le_visage' ],
    [ 'Je me lève a huit heure.', 'je_me_leve_a_huit_heure' ],
    [ 'Marion a trois frères.', 'marion_a_trois_freres' ],
    [ 'Le ciel est gris aujourd\'hui', 'le_ciel_est_gris_aujourdhui' ],
    [ 'Reconnais-tu l\'écriture de ce document ?', 'reconnais_tu_lecriture_de_ce_document' ],
    [ 'Est-ce un parent à toi ?', 'est_ce_un_parent_a_toi' ],
    [ 'Il n\'y a plus de sucre.', 'il_ny_a_plus_de_sucre' ],
    [ 'C\'est ma chaise.', 'cest_ma_chaise' ],
    [ 'Cette tache est invisible à l\'oeil nu.', 'cette_tache_est_invisible_a_loeil_nu' ],
    [ 'C\'est ma chaise.', 'cest_ma_chaise' ],
    [ 'Dirigez-vous vers la sortie.', 'dirigez_vous_vers_la_sortie' ],
    [ 'Pierre est un garçon très sourriant.', 'pierre_est_un_garcon_tres_sourriant' ],
    [ 'Claire est une fille très gai.', 'claire_est_une_fille_tres_gai' ],
    [ 'Nous pourrons mettre un meuble devant ce mur.', 'nous_pourrons_mettre_un_meuble_devant_ce_mur' ],
    [ 'La route qui passe devant chez moi est très étroite.', 'la_route_qui_passe_devant_chez_moi_est_tres_etroite' ],
    [ 'La tempête a fait une victime.', 'la_tempete_a_fait_une_victime' ],
    [ 'La rosée du matin arrose les plantes.', 'la_rosee_du_matin_arrose_les_plantes' ],
    [ 'C\'est à toi ou à moi.', 'cest_a_toi_ou_a_moi' ],
    [ 'Nous pourrons mettre un meuble devant ce mur.', 'nous_pourrons_mettre_un_meuble_devant_ce_mur' ],
    [ 'Il n\'est pas là parce que le train a du retard.', 'il_nest_pas_la_parce_que_le_train_a_du_retard' ]
]


class TestSound(TestCase):
    def __del__(self, *args, **kwargs):
        shutil.rmtree(temp_path)

    def test_sounds(self):
        for sound in sounds:
            text = sound[0]
            file_name = sound[1]
            create_sound(text, file_name)
            print(tmp_sum(file_name) + ' %s' % file_name)
            print(asset_sum(file_name) + ' %s' % file_name)
            self.assertEqual(
                tmp_sum(file_name) + ' %s' % file_name,
                asset_sum(file_name) + ' %s' % file_name
            )
